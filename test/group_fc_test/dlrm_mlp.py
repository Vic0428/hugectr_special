"""
 Copyright (c) 2023, NVIDIA CORPORATION.
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import hugectr
from mpi4py import MPI

# 1. Create Solver, DataReaderParams and Optimizer
solver = hugectr.CreateSolver(
    model_name="dlrm",
    max_eval_batches=300,
    batchsize_eval=16384,
    batchsize=16384,
    lr=0.001,
    vvgpu=[[0]],
    repeat_dataset=True,
    use_mixed_precision=True,
    use_cuda_graph=True,
    scaler=1024,
)
reader = hugectr.DataReaderParams(
    data_reader_type=hugectr.DataReaderType_t.Norm,
    source=["./dcn_data/file_list.txt"],
    eval_source="./dcn_data/file_list_test.txt",
    check_type=hugectr.Check_t.Sum,
)
optimizer = hugectr.CreateOptimizer(
    optimizer_type=hugectr.Optimizer_t.Adam,
    update_type=hugectr.Update_t.Global,
    beta1=0.9,
    beta2=0.999,
    epsilon=0.0001,
)
# 2. Initialize the Model instance
model = hugectr.Model(solver, reader, optimizer)
model.add(
    hugectr.Input(
        label_dim=1,
        label_name="label",
        dense_dim=13,
        dense_name="dense",
        data_reader_sparse_param_array=[hugectr.DataReaderSparseParam("data1", 1, True, 26)],
    )
)
compute_config = hugectr.DenseLayerComputeConfig(
    async_wgrad=True,
)
model.add(
    hugectr.SparseEmbedding(
        embedding_type=hugectr.Embedding_t.DistributedSlotSparseEmbeddingHash,
        workspace_size_per_gpu_in_mb=2400,
        embedding_vec_size=128,
        combiner="sum",
        sparse_embedding_name="sparse_embedding1",
        bottom_name="data1",
        optimizer=optimizer,
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.MLP,
        bottom_names=["dense"],
        top_names=["mlp1"],
        num_outputs=[512, 256, 128],
        compute_config=compute_config,
        act_type=hugectr.Activation_t.Relu,
        use_bias=True,
        # activations = [hugectr.Activation_t.Relu, hugectr.Activation_t.Relu, hugectr.Activation_t.Relu, hugectr.Activation_t.Relu, hugectr.Activation_t.Non],
        # biases = [True, True, True],
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.Interaction,
        bottom_names=["mlp1", "sparse_embedding1"],
        top_names=["interaction1", "interaction_grad"],
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.MLP,
        bottom_names=["interaction1", "interaction_grad"],
        top_names=["mlp2"],
        num_outputs=[1024, 1024, 512, 256, 1],
        compute_config=compute_config,
        use_bias=True,
        activations=[
            hugectr.Activation_t.Relu,
            hugectr.Activation_t.Relu,
            hugectr.Activation_t.Relu,
            hugectr.Activation_t.Relu,
            hugectr.Activation_t.Non,
        ],
        # biases = [True, True, True, True, True],
    )
)
model.add(
    hugectr.DenseLayer(
        layer_type=hugectr.Layer_t.BinaryCrossEntropyLoss,
        bottom_names=["mlp2", "label"],
        top_names=["loss"],
    )
)
model.graph_to_json("dlrm.json")
model.compile()
model.summary()
model.fit(max_iter=2300, display=200, eval_interval=1000, snapshot=200000, snapshot_prefix="dlrm")
