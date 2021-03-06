// GENERATED FILE - DO NOT EDIT.
// Generated by gen_vk_internal_shaders.py.
//
// Copyright 2018 The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// shaders/gen/ConvertIndex.comp.00000001.inc:
//   Pre-generated shader for the ANGLE Vulkan back-end.

#pragma once
constexpr uint8_t kConvertIndex_comp_00000001[] = {
    0x1f,0x8b,0x08,0x00,0x00,0x00,0x00,0x00,0x02,0xff,0x6d,0x94,0xdd,0x4b,0xd3,0x61,
    0x14,0xc7,0x9f,0xfd,0x36,0xa7,0xbd,0xd0,0x0b,0x69,0x6e,0x50,0xdb,0x6c,0x74,0x63,
    0xa1,0x21,0x19,0x8d,0x28,0xea,0x42,0x4c,0x98,0x96,0x0c,0x82,0xf2,0x2a,0xe8,0xa6,
    0x8b,0x32,0xda,0xfe,0x80,0xb6,0x56,0x10,0xa6,0xfd,0x01,0x15,0x15,0x81,0x95,0x48,
    0x84,0x74,0x1d,0x26,0xc6,0x8a,0xd8,0x95,0xe4,0x4d,0x2f,0xff,0x45,0xf4,0x46,0xd8,
    0x39,0x8f,0x9f,0xc7,0x4e,0xd2,0xe0,0x70,0x9e,0xf3,0x3d,0xef,0xdf,0xe7,0xf9,0x2d,
    0x1e,0xe5,0x5b,0x9d,0x8b,0xb9,0x8d,0xae,0xcd,0x7d,0x71,0xab,0xbf,0xed,0x2e,0x12,
    0xc4,0xb9,0x4d,0x2e,0xe9,0xf5,0x60,0xb1,0x54,0xec,0x29,0x57,0x2e,0xf4,0x1c,0xec,
    0x3f,0xa0,0xfe,0x2d,0x2e,0xee,0xe3,0xd4,0xb7,0x55,0x62,0x5a,0x44,0x27,0x44,0x2e,
    0x9d,0xbf,0x78,0x59,0xf1,0x11,0x91,0x6d,0x82,0x27,0x7c,0x2d,0xe7,0x8e,0x13,0xab,
    0x72,0x52,0xa2,0xdb,0xe9,0x93,0x47,0x07,0x2c,0x06,0x96,0x30,0x58,0x04,0xd6,0x66,
    0xb0,0x38,0xd8,0x66,0x9d,0x4d,0xac,0x10,0x37,0x28,0x99,0x19,0xd1,0xc9,0xb5,0x1a,
    0x09,0x97,0xa5,0x47,0x8a,0xfc,0xec,0xba,0xde,0x9a,0x9f,0xa5,0xa6,0xe6,0x77,0x89,
    0xde,0xb3,0xe6,0x5b,0xb5,0xbb,0x98,0x4d,0xed,0x11,0xcf,0x8b,0x73,0xbb,0xb0,0xab,
    0xff,0xf4,0x6b,0x71,0xb5,0xff,0xd4,0xaf,0x99,0xfa,0xf5,0x75,0xf5,0xeb,0xd4,0x0f,
    0xf6,0x24,0xf5,0xd3,0x22,0x3b,0x64,0xab,0xc8,0xfb,0xe3,0x3e,0x5f,0xcf,0x1d,0x12,
    0xa3,0xfd,0x72,0xe4,0x64,0xc4,0x6a,0x67,0x06,0x2b,0x39,0x89,0xeb,0x10,0xbd,0x41,
    0x44,0xfd,0x47,0xb0,0x77,0x82,0x69,0x9d,0x4e,0xea,0xe8,0x6e,0xfb,0xb0,0x53,0xd4,
    0xd5,0xfc,0x34,0xb1,0x5a,0x6f,0xb7,0x4c,0x10,0xb8,0xcd,0xc0,0x59,0x86,0xb8,0x1c,
    0xb3,0x65,0xe9,0x93,0x63,0xa7,0xc8,0xd4,0xcd,0x63,0x6b,0xfc,0x5e,0xce,0x49,0xfc,
    0xaa,0xbb,0xe1,0x28,0xc4,0xf7,0x1a,0x5b,0xfd,0x7d,0x22,0x2b,0x7e,0x97,0xc8,0xf5,
    0x1b,0xbc,0xa0,0xf8,0xca,0x5f,0x7b,0x80,0xf9,0x3b,0xc5,0x2e,0xd2,0x23,0x4e,0xdf,
    0x61,0x76,0x2d,0x32,0xe7,0x30,0x6f,0x35,0x86,0xff,0x14,0xe7,0xa4,0x99,0xa3,0x64,
    0xf8,0x51,0x7c,0x1c,0x5b,0xf9,0xa8,0x1a,0x3e,0xf4,0x8e,0xab,0xd4,0xb9,0xce,0x7e,
    0x35,0xfa,0xa8,0x5d,0x37,0x7c,0x68,0xce,0x6d,0xbe,0x8b,0xfd,0x62,0xe9,0x3c,0x93,
    0x60,0xe3,0x48,0x88,0x5b,0xf6,0xdf,0x92,0x73,0x87,0xe4,0x6d,0x45,0xbc,0x33,0xc7,
    0x4e,0xdf,0x05,0xd1,0x6f,0xef,0x9b,0x58,0x53,0xe0,0xbf,0xe4,0xac,0x1c,0xdc,0xc1,
    0xaf,0xfa,0x84,0x44,0xa5,0xfd,0xfb,0x5c,0xbd,0x7f,0xbd,0x8b,0xa3,0xd4,0x1f,0x02,
    0xd7,0x18,0xdd,0xff,0x34,0x9c,0x0c,0x98,0x98,0x51,0xf0,0x45,0x89,0x51,0xfb,0x0c,
    0x98,0x72,0xf3,0x5c,0x30,0xbd,0x8f,0xb3,0xe0,0x43,0xcc,0x33,0xc6,0x3c,0x3f,0xa5,
    0x86,0xfa,0xce,0x89,0x8c,0x31,0x93,0x9e,0x7f,0x88,0x9e,0xc2,0x1e,0x33,0x33,0xde,
    0x65,0xc6,0x94,0xe9,0x7f,0x0f,0xfc,0x1a,0xfd,0xef,0xd3,0x4b,0xf1,0x05,0xb0,0x07,
    0xe0,0x79,0x5f,0x2b,0xe9,0xdf,0xd8,0x43,0xde,0x61,0x0a,0x7f,0xa8,0xf7,0x08,0x5f,
    0x83,0xdc,0xc7,0xe4,0x76,0x9b,0x1d,0xa7,0xc1,0x7b,0x4d,0x8f,0x27,0xe4,0x4e,0x9b,
    0xdc,0xa7,0xe0,0xfa,0x3e,0x67,0xe0,0x62,0x06,0xbc,0x8f,0x3d,0x67,0xd9,0x53,0xf5,
    0x33,0xc9,0xd2,0xbc,0x4f,0xc4,0x15,0x88,0x0d,0x7d,0xe7,0xf0,0x29,0xff,0x6f,0xc0,
    0x5e,0x62,0xcf,0x19,0x0e,0xae,0xc0,0x81,0xbe,0x95,0x17,0xf4,0xbd,0x0a,0x1e,0xee,
    0xa0,0x62,0xee,0x40,0x7d,0x65,0x91,0x0a,0xb3,0x94,0x4d,0xad,0x57,0xe4,0x59,0x3e,
    0xe7,0xc1,0x2d,0x9f,0xaf,0x0d,0x9f,0xf3,0x86,0xcf,0x05,0x7c,0x81,0x93,0x45,0x72,
    0x2d,0x9f,0x0d,0x70,0xcb,0xe7,0x5b,0x72,0x1b,0x26,0xf7,0x1d,0xb8,0xe5,0xf3,0x3d,
    0x78,0xe0,0xb3,0xc9,0x0e,0x4d,0xc3,0xe7,0x67,0xe2,0x0a,0xc4,0x86,0xbe,0x4b,0xf8,
    0x96,0x0d,0x9f,0x1f,0xe0,0x74,0x89,0x7a,0x81,0x13,0xd5,0x5f,0x5d,0xab,0x8f,0xf9,
    0x48,0xcc,0x2c,0xf1,0x4d,0xf3,0x46,0x6f,0xf0,0x46,0x4b,0x86,0x83,0x9b,0xe0,0x81,
    0xd3,0x5b,0x60,0xa3,0x86,0xbf,0x09,0xfe,0x07,0x52,0xf8,0x8f,0xc9,0x1d,0x4d,0xd0,
    0xcb,0x7e,0x0f,0xaa,0x7f,0xcb,0xbf,0xcc,0x61,0x91,0x3f,0xc3,0x99,0xfa,0xf6,0xa0,
    0x07,0x00,0x00
};

// Generated from:
//
// #version 450 core
//
// layout(local_size_x = 64, local_size_y = 1, local_size_z = 1)in;
//
// layout(set = 0, binding = 0)buffer dst
// {
//
//     uint dstIndexBuf[];
// };
//
// layout(set = 0, binding = 1)readonly buffer src
// {
//
//     uint srcIndexBuf[];
// };
//
// layout(push_constant)uniform PushConstants
// {
//
//     uint srcIndexOffset;
//
//     uint dstIndexBufOffsetDiv4;
//
//     uint maxIndex;
//
//     uint _padding;
// };
//
// uint PullIndex(uint index)
// {
//
//     uint srcIndex = index + srcIndexOffset;
//
//     uint srcBlock = srcIndexBuf[srcIndex >> 2];
//     uint srcComponent =(srcIndex & 3);
//
//     uint value =(srcBlock >>(srcComponent << 3))& 0xFF;
//
//     if(value == 0xFF)
//         value = 0xFFFF;
//
//     return value;
// }
//
// void PackIndexValue(uint srcValue, uint indexIndex, inout uint dstValue)
// {
//
//     dstValue |= srcValue <<(indexIndex << 4);
// }
//
// void main()
// {
//
//     uint firstIndex = 0;
//     uint endIndex = firstIndex + maxIndex;
//
//     uint index =((gl_GlobalInvocationID . x +(firstIndex >> 1))<< 1);
//
//     if(index >= endIndex)
//         return;
//
//     uint dstValue = 0;
//
//     if(index >= firstIndex)
//     {
//         uint srcValue = PullIndex(index);
//         PackIndexValue(srcValue, 0, dstValue);
//     }
//
//     if(index + 1 < endIndex)
//     {
//         uint srcValue = PullIndex(index + 1);
//         PackIndexValue(srcValue, 1, dstValue);
//     }
//
//     dstIndexBuf[dstIndexBufOffsetDiv4 + gl_GlobalInvocationID . x]= dstValue;
//
// }
