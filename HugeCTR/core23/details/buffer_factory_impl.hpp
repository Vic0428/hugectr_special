/*
 * Copyright (c) 2023, NVIDIA CORPORATION.
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

#include <memory>

namespace HugeCTR {

namespace core23 {

class Allocator;
class Device;
class BufferChannel;
class Buffer;
struct BufferParams;

[[nodiscard]] std::shared_ptr<Buffer> CreateBuffer(BufferParams buffer_params, const Device& device,
                                                   std::unique_ptr<Allocator> allocator);

}  // namespace core23

}  // namespace HugeCTR