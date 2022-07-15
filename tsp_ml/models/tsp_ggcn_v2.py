# -*- coding: utf-8 -*-
import torch
import torch.nn.functional as F
from torch_geometric.nn import GatedGraphConv, Linear


class TSP_GGCN_v2(torch.nn.Module):
    def __init__(self):
        super().__init__()
        output_size = 2
        node_hidden_layer_1_size = 100
        node_hidden_layer_2_size = 100
        edge_hidden_layer_1_size = 100
        self.conv_1 = GatedGraphConv(50, num_layers=3)
        self.conv_2 = GatedGraphConv(100, num_layers=3)
        self.conv_3 = GatedGraphConv(150, num_layers=3)
        self.fully_connected_nodes = Linear(in_channels=150, out_channels=150)
        self.fully_connected_edges_1 = Linear(
            150 * 2, out_channels=edge_hidden_layer_1_size
        )
        self.fully_connected_edges_2 = Linear(
            edge_hidden_layer_1_size, out_channels=output_size
        )

    def forward(self, data):
        node_positions = data.features
        edge_index = data.edge_index
        edge_weights = data.distance

        # propagate node features
        node_features = self.conv_1(node_positions, edge_index, edge_weights)
        node_features = F.relu(node_features)
        node_features = F.dropout(node_features, training=self.training)
        node_features = self.conv_2(node_features, edge_index, edge_weights)
        node_features = F.relu(node_features)
        node_features = F.dropout(node_features, training=self.training)
        node_features = self.conv_3(node_features, edge_index, edge_weights)
        node_features = F.relu(node_features)
        node_features = F.dropout(node_features, training=self.training)
        node_features = self.fully_connected_nodes(node_features)
        node_features = F.relu(node_features)

        # generate edge features and calculate one score for each edge
        src, dst = data.edge_index
        edge_features = torch.cat((node_features[src], node_features[dst]), 1)
        edge_features = self.fully_connected_edges_1(edge_features)
        edge_scores = self.fully_connected_edges_2(edge_features)

        return edge_scores
