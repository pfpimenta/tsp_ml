# -*- coding: utf-8 -*-
import torch
from greedy import greedy
from torch import Tensor
from torch_geometric.data import Batch


class GreedyModel(torch.nn.Module):
    """Greedy deterministic heuristic"""

    def __init__(self):
        super().__init__()

    def forward(self, data: Batch) -> Tensor:
        edge_scores = data.edge_weights.view(-1, 1)
        # score for negative class == 1 - score
        edge_scores = edge_scores.repeat(1, 2)
        edge_scores[:, 1] = 1 - edge_scores[:, 1]
        return edge_scores

    def predict(self, scores: Tensor, edge_index: Tensor) -> Tensor:
        solution = greedy(edge_scores=scores, edge_index=edge_index)
        return solution
