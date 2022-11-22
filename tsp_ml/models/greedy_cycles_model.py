# -*- coding: utf-8 -*-
import torch
from greedy import greedy
from torch import Tensor
from torch_geometric.data import Batch


class GreedyCyclesModel(torch.nn.Module):
    """Greedy deterministic heuristic that only finds cycles
    made only with PDP (patient-donor pairs) nodes"""

    def __init__(self):
        super().__init__()

    def forward(self, data: Batch) -> Tensor:
        edge_scores = data.edge_weights.view(-1, 1)
        # score for negative class = 1 - score
        edge_scores = edge_scores.repeat(1, 2)
        edge_scores[:, 1] = 1 - edge_scores[:, 1]
        return edge_scores

    def predict(self, data: Batch) -> Tensor:
        solution = greedy(
            edge_scores=data.scores,
            edge_index=data.edge_index,
            node_types=data.type[0],
            greedy_algorithm="greedy_cycles",
        )
        return solution
