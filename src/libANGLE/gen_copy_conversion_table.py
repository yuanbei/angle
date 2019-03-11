#!/usr/bin/python
# Copyright 2016 The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# gen_copy_conversion_table.py:
#  Code generation for ES3 valid copy conversions table format map.
#  NOTE: don't run this script directly. Run scripts/run_code_generation.py.

from datetime import date
import sys

sys.path.append('renderer')
import angle_format

template_cpp = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {data_source_name}.
//
// Copyright {copyright_year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// format_map:
//   Determining the sized internal format from a (format,type) pair.
//   Also check es3 format combinations for validity.

#include "angle_gl.h"
#include "common/debug.h"

namespace gl
{{

bool ValidES3CopyConversion(GLenum textureFormat, GLenum framebufferFormat)
{{
    switch (textureFormat)
    {{
{texture_format_cases}        default:
            break;
    }}

    return false;
}}

}}  // namespace gl
"""

template_format_case = """        case {texture_format}:
            switch (framebufferFormat)
            {{
{framebuffer_format_cases}                    return true;
                default:
                    break;
            }}
            break;

"""

template_simple_case = """                case {key}:
"""

def parse_texture_format_case(texture_format, framebuffer_formats):
    framebuffer_format_cases = ""
    for framebuffer_format in sorted(framebuffer_formats):
        framebuffer_format_cases += template_simple_case.format(key = framebuffer_format)
    return template_format_case.format(
        texture_format = texture_format, framebuffer_format_cases = framebuffer_format_cases)


def main():

    data_source_name = 'es3_copy_conversion_formats.json'
    out_file_name = 'es3_copy_conversion_table_autogen.cpp'

    # auto_script parameters.
    if len(sys.argv) > 1:
        inputs = [data_source_name]
        outputs = [out_file_name]

        if sys.argv[1] == 'inputs':
            print ','.join(inputs)
        elif sys.argv[1] == 'outputs':
            print ','.join(outputs)
        else:
            print('Invalid script parameters')
            return 1
        return 0

    json_data = angle_format.load_json(data_source_name)

    format_map = {}

    for description, data in json_data.iteritems():
        for texture_format, framebuffer_format in data:
            if texture_format not in format_map:
                format_map[texture_format] = []
            format_map[texture_format] += [ framebuffer_format ]

    texture_format_cases = ""

    for texture_format, framebuffer_formats in sorted(format_map.iteritems()):
        texture_format_cases += parse_texture_format_case(texture_format, framebuffer_formats)

    with open(out_file_name, 'wt') as out_file:
        output_cpp = template_cpp.format(
            script_name = sys.argv[0],
            data_source_name = data_source_name,
            copyright_year = date.today().year,
            texture_format_cases = texture_format_cases)
        out_file.write(output_cpp)
        out_file.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
