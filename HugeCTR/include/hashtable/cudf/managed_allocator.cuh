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

#include <base/debug/logger.hpp>
using HugeCTR::Logger;

template <class T>
struct managed_allocator {
  typedef T value_type;

  managed_allocator() = default;

  template <class U>
  constexpr managed_allocator(const managed_allocator<U>&) noexcept {}

  T* allocate(std::size_t n) const {
    T* ptr = nullptr;
    cudaError_t result = cudaMallocManaged(&ptr, n * sizeof(T));
    if (cudaSuccess != result || nullptr == ptr) {
      HCTR_LOG_S(ERROR, WORLD) << "CUDA Runtime call in line " << __LINE__ << " of file "
                               << __FILE__ << " failed with " << cudaGetErrorString(result) << " ("
                               << result << "). Attempted to allocate: " << n * sizeof(T)
                               << " bytes." << std::endl;
      throw std::bad_alloc();
    }
    return ptr;
  }
  void deallocate(T* p, std::size_t) const { cudaFree(p); }
};

template <class T, class U>
bool operator==(const managed_allocator<T>&, const managed_allocator<U>&) {
  return true;
}
template <class T, class U>
bool operator!=(const managed_allocator<T>&, const managed_allocator<U>&) {
  return false;
}
