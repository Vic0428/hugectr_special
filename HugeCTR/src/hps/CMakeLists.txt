#
# Copyright (c) 2023, NVIDIA CORPORATION.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

cmake_minimum_required(VERSION 3.8)
set(DB_LIB_PATHS "/usr/local/lib" CACHE PATH "Paths to Hiredis/rocksdb lib")

file(GLOB_RECURSE huge_ctr_hps_src RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} *.cpp *.cu)

list(APPEND huge_ctr_hps_src 
  "../utils.cu"
  "../base/debug/logger.cpp"
  "../base/debug/cuda_debugging.cu"
  "../thread_pool.cpp"
  "../io/filesystem.cpp"
  "../io/local_filesystem.cpp"
  "../io/hadoop_filesystem.cpp"
  "../io/s3_filesystem.cpp"
  "../io/gcs_filesystem.cpp"
)

set(CMAKE_CXX_STANDARD 17)
add_library(huge_ctr_hps SHARED ${huge_ctr_hps_src})

if(ENABLE_HDFS)
  target_link_libraries(
    huge_ctr_hps
    PUBLIC
      ${DB_LIB_PATHS}/libhdfs.so # from Hugectr
  )
endif()

if(ENABLE_S3)
  target_link_libraries(
    huge_ctr_hps
    PUBLIC
      ${DB_LIB_PATHS}/libaws-cpp-sdk-core.so ${DB_LIB_PATHS}/libaws-cpp-sdk-s3.so # from Hugectr
  )
endif()

if(ENABLE_GCS)
  target_link_libraries(
    huge_ctr_hps
    PUBLIC
      ${DB_LIB_PATHS}/libgoogle_cloud_cpp_common.so ${DB_LIB_PATHS}/libgoogle_cloud_cpp_rest_internal.so ${DB_LIB_PATHS}/libgoogle_cloud_cpp_storage.so
  )
endif()

target_link_libraries(huge_ctr_hps PUBLIC gpu_cache tbb hiredis redis++ rocksdb-shared rdkafka)

target_compile_features(huge_ctr_hps PUBLIC cxx_std_17)
target_link_libraries(huge_ctr_hps PUBLIC numa )

set_target_properties(huge_ctr_hps PROPERTIES CUDA_RESOLVE_DEVICE_SYMBOLS ON)

set_target_properties(huge_ctr_hps PROPERTIES CUDA_ARCHITECTURES OFF)
