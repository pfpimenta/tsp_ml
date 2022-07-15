# -*- coding: utf-8 -*-
import sys

import torch
from definitions import (
    TEST_DATASET_FOLDER_PATH,
    TRAIN_DATASET_FOLDER_PATH,
    TRAINED_MODELS_FOLDER_PATH,
)
from model_utils import get_model_name, load_model
from torch_geometric.loader import DataLoader
from tqdm import tqdm
from tsp_dataset import TSPDataset

from model_performance import ModelPerformance

# MODEL_FILENAME = "tsp_gcn_model.pt"
# MODEL_FILENAME = "TSP_GGCN_2022_07_05_16h31.pt"
# MODEL_FILENAME = "TSP_GGCN_2022_07_07_17h56.pt"
# MODEL_FILENAME = "TSP_GGCN_2022_07_07_19h40.pt"
# MODEL_FILENAME = "TSP_GGCN_2022_07_08_17h00.pt"
# MODEL_FILENAME = "TSP_GGCN_2022_07_12_12h27.pt"
# MODEL_FILENAME = "TSP_GGCN_v2_2022_07_14_23h00.pt"
MODEL_FILENAME = "TSP_GGCN_v2_2022_07_14_23h00"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device}")


def evaluate(model: torch.nn.Module, dataset: TSPDataset) -> ModelPerformance:
    model_performance = ModelPerformance()
    dataloader = DataLoader(
        dataset, shuffle=True, batch_size=batch_size, pin_memory=True, num_workers=4
    )
    model.eval()  # set the model to evaluation mode
    for i, batch in enumerate(tqdm(dataloader, desc="Evaluation", file=sys.stdout)):
        batch = batch.to(device)
        label = batch.y
        label = label.to(torch.float32)
        scores = model(batch)
        pred = torch.argmax(scores, 1).to(int)
        model_performance.update(pred=pred, truth=batch.y)
        if i == 30:
            pass
            # import pdb
            # pdb.set_trace()

    dataset_size = len(dataset)
    print(f"Dataset size: {dataset_size}")
    print(f"Dataset total num_edges: {dataset.num_edges}")
    avg_num_edges = int(dataset.num_edges) / int(dataset_size)
    print(f"Mean num_edges per graph: {avg_num_edges}")
    model_performance.print()
    return model_performance


if __name__ == "__main__":
    # select either CPU or GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using {device}")

    # # load model
    # model = TSP_GGCN().to(device)
    # model_filepath = TRAINED_MODELS_FOLDER_PATH / MODEL_FILENAME
    # print(f"...Loading model from file {model_filepath}")
    # model.load_state_dict(torch.load(model_filepath, map_location=device))

    # setup data
    batch_size = 10
    train_dataset = TSPDataset(dataset_folderpath=TRAIN_DATASET_FOLDER_PATH)
    test_dataset = TSPDataset(dataset_folderpath=TEST_DATASET_FOLDER_PATH)

    model = load_model(model_name="TSP_GGCN_v2_2022_07_14_23h00")
    model_name = get_model_name(model=model)
    print("\n\nEvaluating the model on the train dataset")
    train_model_performance = evaluate(model=model, dataset=train_dataset)
    train_model_performance.save(output_filename="train_" + model_name)
    print("\n\nEvaluating the model on the test dataset")
    test_model_performance = evaluate(model=model, dataset=test_dataset)
    test_model_performance.save(output_filename="test_" + model_name)
