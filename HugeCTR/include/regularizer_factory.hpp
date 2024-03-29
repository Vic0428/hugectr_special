/* * Copyright (c) 2023, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#pragma once

#include <common.hpp>
#include <core23/tensor_container.hpp>
#include <gpu_resource.hpp>
#include <memory>
#include <regularizer.hpp>

namespace HugeCTR {

template <typename T>
std::shared_ptr<Regularizer<T>> create_regularizer(
    bool use_regularizer, Regularizer_t regularizer_type, float lambda,
    std::vector<core23::Tensor> weight_tensors, std::vector<core23::Tensor> wgrad_tensors,
    const int batch_size, const std::shared_ptr<GPUResource>& gpu_resource);

}  // namespace HugeCTR