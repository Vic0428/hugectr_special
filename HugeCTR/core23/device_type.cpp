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

#include <base/debug/logger.hpp>
#include <core23/device_type.hpp>
#include <string>

namespace HugeCTR {

namespace core23 {

namespace {
#define DEVICE_NAMEOF(D) #D,

constexpr const char *device_type_name[] = {ALL_DEVICE_TYPES_SUPPORTED(DEVICE_NAMEOF)};

}  // namespace

std::string GetDeviceTypeName(DeviceType device_type) {
  return device_type_name[static_cast<std::underlying_type_t<DeviceType>>(device_type)];
}

std::ostream &operator<<(std::ostream &os, DeviceType device_type) {
  os << GetDeviceTypeName(device_type);
  return os;
}

}  // namespace core23
}  // namespace HugeCTR
