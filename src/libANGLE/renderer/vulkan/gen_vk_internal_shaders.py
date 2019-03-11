#!/usr/bin/python
# Copyright 2018 The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# gen_vk_internal_shaders.py:
#  Code generation for internal Vulkan shaders. Should be run when an internal
#  shader program is changed, added or removed.
#  Because this script can be slow direct invocation is supported. But before
#  code upload please run scripts/run_code_generation.py.

from datetime import date
import json
import os
import re
import subprocess
import sys

out_file_cpp = 'vk_internal_shaders_autogen.cpp'
out_file_h = 'vk_internal_shaders_autogen.h'
out_file_gni = 'vk_internal_shaders_autogen.gni'

# Templates for the generated files:
template_shader_library_cpp = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {input_file_name}
//
// Copyright {copyright_year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// {out_file_name}:
//   Pre-generated shader library for the ANGLE Vulkan back-end.

#include "libANGLE/renderer/vulkan/vk_internal_shaders_autogen.h"

namespace rx
{{
namespace vk
{{
namespace
{{
{internal_shader_includes}

// This is SPIR-V binary blob and the size.
struct ShaderBlob
{{
    const uint32_t *code;
    size_t codeSize;
}};

{shader_tables_cpp}

angle::Result GetShader(Context *context,
                        RefCounted<ShaderAndSerial> *shaders,
                        const ShaderBlob *shaderBlobs,
                        size_t shadersCount,
                        uint32_t shaderFlags,
                        RefCounted<ShaderAndSerial> **shaderOut)
{{
    ASSERT(shaderFlags < shadersCount);
    RefCounted<ShaderAndSerial> &shader = shaders[shaderFlags];
    *shaderOut                          = &shader;

    if (shader.get().valid())
    {{
        return angle::Result::Continue;
    }}

    // Create shader lazily. Access will need to be locked for multi-threading.
    const ShaderBlob &shaderCode = shaderBlobs[shaderFlags];
    ASSERT(shaderCode.code != nullptr);

    return InitShaderAndSerial(context, &shader.get(), shaderCode.code, shaderCode.codeSize);
}}
}}  // anonymous namespace


ShaderLibrary::ShaderLibrary()
{{
}}

ShaderLibrary::~ShaderLibrary()
{{
}}

void ShaderLibrary::destroy(VkDevice device)
{{
    {shader_destroy_calls}
}}

{shader_get_functions_cpp}
}}  // namespace vk
}}  // namespace rx
"""

template_shader_library_h = """// GENERATED FILE - DO NOT EDIT.
// Generated by {script_name} using data from {input_file_name}
//
// Copyright {copyright_year} The ANGLE Project Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// {out_file_name}:
//   Pre-generated shader library for the ANGLE Vulkan back-end.

#ifndef LIBANGLE_RENDERER_VULKAN_VK_INTERNAL_SHADERS_AUTOGEN_H_
#define LIBANGLE_RENDERER_VULKAN_VK_INTERNAL_SHADERS_AUTOGEN_H_

#include "libANGLE/renderer/vulkan/vk_utils.h"

namespace rx
{{
namespace vk
{{
namespace InternalShader
{{
{shader_variation_definitions}
}}  // namespace InternalShader

class ShaderLibrary final : angle::NonCopyable
{{
  public:
    ShaderLibrary();
    ~ShaderLibrary();

    void destroy(VkDevice device);

    {shader_get_functions_h}

  private:
    {shader_tables_h}
}};
}}  // namespace vk
}}  // namespace rx

#endif  // LIBANGLE_RENDERER_VULKAN_VK_INTERNAL_SHADERS_AUTOGEN_H_
"""

template_shader_includes_gni = """# GENERATED FILE - DO NOT EDIT.
# Generated by {script_name} using data from {input_file_name}
#
# Copyright {copyright_year} The ANGLE Project Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# {out_file_name}:
#   List of generated shaders for inclusion in ANGLE's build process.

angle_vulkan_internal_shaders = [
{shaders_list}
]
"""

# Gets the constant variable name for a generated shader.
def get_var_name(output, prefix='k'):
    return prefix + output.replace(".", "_")

# Gets the namespace name given to constants generated from shader_file
def get_namespace_name(shader_file):
    return get_var_name(os.path.basename(shader_file), '')

# Gets the namespace name given to constants generated from shader_file
def get_variation_table_name(shader_file, prefix='k'):
    return get_var_name(os.path.basename(shader_file), prefix) + '_shaders'

# Gets the internal ID string for a particular shader.
def get_shader_id(shader):
    file = os.path.splitext(os.path.basename(shader))[0]
    return file.replace(".", "_")

# Returns the name of the generated SPIR-V file for a shader.
def get_output_path(name):
    return os.path.join('shaders', 'gen', name + ".inc")

# Finds a path to GN's out directory
def find_build_path(path):
    out = os.path.join(path, "out")
    if (os.path.isdir(out)):
        for o in os.listdir(out):
            subdir = os.path.join(out, o)
            if os.path.isdir(subdir):
                argsgn = os.path.join(subdir, "args.gn")
                if os.path.isfile(argsgn):
                    return subdir
    else:
        parent = os.path.join(path, "..")
        if (os.path.isdir(parent)):
            return find_build_path(parent)
        else:
            raise Exception("Could not find GN out directory")

# Generates the code for a shader blob array entry.
def gen_shader_blob_entry(shader):
    var_name = get_var_name(os.path.basename(shader))[0:-4]
    return "{%s, %s}" % (var_name, "sizeof(%s)" % var_name)

def slash(s):
    return s.replace('\\', '/')

def gen_shader_include(shader):
    return '#include "libANGLE/renderer/vulkan/%s"' % slash(shader)

def get_shader_variations(shader):
    variation_file = shader + '.json'
    if not os.path.exists(variation_file):
        # If there is no variation file, assume none.
        return ({}, [])

    with open(variation_file) as fin:
        variations = json.loads(fin.read())
        flags = {}
        enums = []

        for key, value in variations.iteritems():
            if key == "Description":
                continue
            elif key == "Flags":
                flags = value
            elif len(value) > 0:
                enums.append((key, value))

        # sort enums so the ones with the most waste ends up last, reducing the table size
        enums.sort(key=lambda enum: (1 << (len(enum[1]) - 1).bit_length()) / float(len(enum[1])))

        return (flags, enums)

def get_variation_bits(flags, enums):
    flags_bits = len(flags)
    enum_bits = [(len(enum[1]) - 1).bit_length() for enum in enums]
    return (flags_bits, enum_bits)

def next_enum_variation(enums, enum_indices):
    """Loop through indices from [0, 0, ...] to [L0-1, L1-1, ...]
    where Li is len(enums[i]).  The list can be thought of as a number with many
    digits, where each digit is in [0, Li), and this function effectively implements
    the increment operation, with the least-significant digit being the first item."""
    for i in range(len(enums)):
        current = enum_indices[i]
        # if current digit has room, increment it.
        if current + 1 < len(enums[i][1]):
            enum_indices[i] = current + 1
            return True;
        # otherwise reset it to 0 and carry to the next digit.
        enum_indices[i] = 0

    # if this is reached, the number has overflowed and the loop is finished.
    return False

compact_newlines_regex = re.compile(r"\n\s*\n", re.MULTILINE)
def cleanup_preprocessed_shader(shader_text):
    return compact_newlines_regex.sub('\n\n', shader_text.strip())

def compile_variation(glslang_path, shader_file, shader_basename, flags, enums,
        flags_active, enum_indices, flags_bits, enum_bits, output_shaders):

    glslang_args = [glslang_path]

    # generate -D defines and the output file name
    #
    # The variations are given a bit pattern to be able to OR different flags into a variation. The
    # least significant bits are the flags, where there is one bit per flag.  After that, each enum
    # takes up as few bits as needed to count that many enum values.
    variation_bits = 0
    variation_string = ''
    for f in range(len(flags)):
        if flags_active & (1 << f):
            flag_name = flags[f]
            glslang_args.append('-D' + flag_name + '=1')

            variation_bits |= 1 << f
            variation_string += '|' + flag_name

    current_bit_start = flags_bits

    for e in range(len(enums)):
        enum_name = enums[e][1][enum_indices[e]]
        glslang_args.append('-D' + enum_name + '=1')

        variation_bits |= enum_indices[e] << current_bit_start
        current_bit_start += enum_bits[e]
        variation_string += '|' + enum_name

    output_name = '%s.%08X' % (shader_basename, variation_bits)
    output_path = get_output_path(output_name)
    output_shaders.append(output_path)

    if glslang_path is not None:
        glslang_preprocessor_output_args = glslang_args + ['-E']
        glslang_preprocessor_output_args.append(shader_file)           # Input GLSL shader

        glslang_args += ['-V']                                         # Output mode is Vulkan
        glslang_args += ['--variable-name', get_var_name(output_name)] # C-style variable name
        glslang_args += ['-o', output_path]                            # Output file
        glslang_args.append(shader_file)                               # Input GLSL shader

        print output_path + ': ' + shader_basename + variation_string
        result = subprocess.call(glslang_args)
        if result != 0:
            raise Exception("Error compiling " + shader_file)

        with open(output_path, 'ab') as incfile:
            shader_text = subprocess.check_output(glslang_preprocessor_output_args)

            incfile.write('\n\n#if 0  // Generated from:\n')
            incfile.write(cleanup_preprocessed_shader(shader_text))
            incfile.write('\n#endif  // Preprocessed code\n')

class ShaderAndVariations:
    def __init__(self, shader_file):
        self.shader_file = shader_file
        (self.flags, self.enums) = get_shader_variations(shader_file)
        get_variation_bits(self.flags, self.enums)
        (self.flags_bits, self.enum_bits) = get_variation_bits(self.flags, self.enums)


def get_variation_definition(shader_and_variation):
    shader_file = shader_and_variation.shader_file
    flags = shader_and_variation.flags
    enums = shader_and_variation.enums
    flags_bits = shader_and_variation.flags_bits
    enum_bits = shader_and_variation.enum_bits

    namespace_name = get_namespace_name(shader_file)

    definition = 'namespace %s\n{\n' % namespace_name
    if len(flags) > 0:
        definition += 'enum flags\n{\n'
        definition += ''.join(['k%s = 0x%08X,\n' % (flags[f], 1 << f) for f in range(len(flags))])
        definition += 'kFlagsMask = 0x%08X,\n' % ((1 << flags_bits) - 1)
        definition += '};\n'

    current_bit_start = flags_bits

    for e in range(len(enums)):
        enum = enums[e]
        enum_name = enum[0]
        definition += 'enum %s\n{\n' % enum_name
        definition += ''.join(['k%s = 0x%08X,\n' %
            (enum[1][v], v << current_bit_start) for v in range(len(enum[1]))])
        definition += 'k%sMask = 0x%08X,\n' % (enum_name, ((1 << enum_bits[e]) - 1) << current_bit_start)
        definition += '};\n'
        current_bit_start += enum_bits[e]

    definition += '}  // namespace %s\n' % namespace_name
    return definition

def get_shader_table_h(shader_and_variation):
    shader_file = shader_and_variation.shader_file
    flags = shader_and_variation.flags
    enums = shader_and_variation.enums

    table_name = get_variation_table_name(shader_file, 'm')

    table = 'RefCounted<ShaderAndSerial> %s[' % table_name

    namespace_name = "InternalShader::" + get_namespace_name(shader_file)

    first_or = True
    if len(flags) > 0:
        table += '%s::kFlagsMask' % namespace_name
        first_or = False

    for e in range(len(enums)):
        enum = enums[e]
        enum_name = enums[e][0]
        if not first_or:
            table += ' | '
        table += '%s::k%sMask' % (namespace_name, enum_name)
        first_or = False

    if first_or:
        table += '1'

    table += '];'
    return table

def get_shader_table_cpp(shader_and_variation):
    shader_file = shader_and_variation.shader_file
    enums = shader_and_variation.enums
    flags_bits = shader_and_variation.flags_bits
    enum_bits = shader_and_variation.enum_bits

    # Cache max and mask value of each enum to quickly know when a possible variation is invalid
    enum_maxes = []
    enum_masks = []
    current_bit_start = flags_bits

    for e in range(len(enums)):
        enum_values = enums[e][1]
        enum_maxes.append((len(enum_values) - 1) << current_bit_start)
        enum_masks.append(((1 << enum_bits[e]) - 1) << current_bit_start)
        current_bit_start += enum_bits[e]

    table_name = get_variation_table_name(shader_file)
    var_name = get_var_name(os.path.basename(shader_file))

    table = 'constexpr ShaderBlob %s[] = {\n' % table_name

    # The last possible variation is every flag enabled and every enum at max
    last_variation = ((1 << flags_bits) - 1) | reduce(lambda x, y: x|y, enum_maxes, 0)

    for variation in range(last_variation + 1):
        # if any variation is invalid, output an empty entry
        if any([(variation & enum_masks[e]) > enum_maxes[e] for e in range(len(enums))]):
            table += '{nullptr, 0}, // 0x%08X\n' % variation
        else:
            entry = '%s_%08X' % (var_name, variation)
            table += '{%s, sizeof(%s)},\n' % (entry, entry)

    table += '};'
    return table

def get_get_function_h(shader_and_variation):
    shader_file = shader_and_variation.shader_file

    function_name = get_var_name(os.path.basename(shader_file), 'get')

    definition = 'angle::Result %s' % function_name
    definition += '(Context *context, uint32_t shaderFlags, RefCounted<ShaderAndSerial> **shaderOut);'

    return definition

def get_get_function_cpp(shader_and_variation):
    shader_file = shader_and_variation.shader_file
    enums = shader_and_variation.enums

    function_name = get_var_name(os.path.basename(shader_file), 'get')
    namespace_name = "InternalShader::" + get_namespace_name(shader_file)
    member_table_name = get_variation_table_name(shader_file, 'm')
    constant_table_name = get_variation_table_name(shader_file)

    definition = 'angle::Result ShaderLibrary::%s' % function_name
    definition += '(Context *context, uint32_t shaderFlags, RefCounted<ShaderAndSerial> **shaderOut)\n{\n'
    definition += 'return GetShader(context, %s, %s, ArraySize(%s), shaderFlags, shaderOut);\n}\n' % (
            member_table_name, constant_table_name, constant_table_name)

    return definition

def get_destroy_call(shader_and_variation):
    shader_file = shader_and_variation.shader_file

    table_name = get_variation_table_name(shader_file, 'm')

    destroy = 'for (RefCounted<ShaderAndSerial> &shader : %s)\n' % table_name
    destroy += '{\nshader.get().destroy(device);\n}'
    return destroy


def main():
    # STEP 0: Handle inputs/outputs for run_code_generation.py's auto_script
    shaders_dir = os.path.join('shaders', 'src')
    if not os.path.isdir(shaders_dir):
        raise Exception("Could not find shaders directory")

    print_inputs = len(sys.argv) == 2 and sys.argv[1] == 'inputs'
    print_outputs = len(sys.argv) == 2 and sys.argv[1] == 'outputs'
    # If an argument X is given that's not inputs or outputs, compile shaders that match *X*.
    # This is useful in development to build only the shader of interest.
    shader_files_to_compile = os.listdir(shaders_dir)
    if not (print_inputs or print_outputs or len(sys.argv) < 2):
        shader_files_to_compile = [f for f in shader_files_to_compile if f.find(sys.argv[1]) != -1]

    valid_extensions = ['.vert', '.frag', '.comp']
    input_shaders = sorted([os.path.join(shaders_dir, shader)
        for shader in os.listdir(shaders_dir)
        if any([os.path.splitext(shader)[1] == ext for ext in valid_extensions])])
    if print_inputs:
        print(",".join(input_shaders))
        sys.exit(0)

    # STEP 1: Call glslang to generate the internal shaders into small .inc files.

    # a) Get the path to the glslang binary from the script directory.
    glslang_path = None
    if not print_outputs:
        build_path = find_build_path(".")
        print("Using glslang_validator from '" + build_path + "'")
        result = subprocess.call(['ninja', '-C', build_path, 'glslang_validator'])
        if result != 0:
            raise Exception("Error building glslang_validator")

        glslang_binary = 'glslang_validator'
        if os.name == 'nt':
            glslang_binary += '.exe'
        glslang_path = os.path.join(build_path, glslang_binary)
        if not os.path.isfile(glslang_path):
            raise Exception("Could not find " + glslang_binary)

    # b) Iterate over the shaders and call glslang with the right arguments.
    output_shaders = []

    input_shaders_and_variations = [ShaderAndVariations(shader_file) for shader_file in input_shaders]

    for shader_and_variation in input_shaders_and_variations:
        shader_file = shader_and_variation.shader_file
        flags = shader_and_variation.flags
        enums = shader_and_variation.enums
        flags_bits = shader_and_variation.flags_bits
        enum_bits = shader_and_variation.enum_bits

        # an array where each element i is in [0, len(enums[i])),
        # telling which enum is currently selected
        enum_indices = [0] * len(enums)

        output_name = os.path.basename(shader_file)

        while True:
            do_compile = not print_outputs and output_name in shader_files_to_compile
            # a number where each bit says whether a flag is active or not,
            # with values in [0, 2^len(flags))
            for flags_active in range(1 << len(flags)):
                compile_variation(glslang_path, shader_file, output_name, flags, enums,
                        flags_active, enum_indices, flags_bits, enum_bits, output_shaders)

            if not next_enum_variation(enums, enum_indices):
                break

    output_shaders = sorted(output_shaders)
    outputs = output_shaders + [out_file_cpp, out_file_h]

    if print_outputs:
        print(','.join(outputs))
        sys.exit(0)

    # STEP 2: Consolidate the .inc files into an auto-generated cpp/h library.
    with open(out_file_cpp, 'w') as outfile:
        includes = "\n".join([gen_shader_include(shader) for shader in output_shaders])
        shader_tables_cpp = '\n'.join([get_shader_table_cpp(s)
            for s in input_shaders_and_variations])
        shader_destroy_calls = '\n'.join([get_destroy_call(s)
            for s in input_shaders_and_variations])
        shader_get_functions_cpp = '\n'.join([get_get_function_cpp(s)
            for s in input_shaders_and_variations])

        outcode = template_shader_library_cpp.format(
            script_name = __file__,
            copyright_year = date.today().year,
            out_file_name = out_file_cpp,
            input_file_name = 'shaders/src/*',
            internal_shader_includes = includes,
            shader_tables_cpp = shader_tables_cpp,
            shader_destroy_calls = shader_destroy_calls,
            shader_get_functions_cpp = shader_get_functions_cpp)
        outfile.write(outcode)
        outfile.close()

    with open(out_file_h, 'w') as outfile:
        shader_variation_definitions = '\n'.join([get_variation_definition(s)
            for s in input_shaders_and_variations])
        shader_get_functions_h = '\n'.join([get_get_function_h(s)
            for s in input_shaders_and_variations])
        shader_tables_h = '\n'.join([get_shader_table_h(s)
            for s in input_shaders_and_variations])
        outcode = template_shader_library_h.format(
            script_name = __file__,
            copyright_year = date.today().year,
            out_file_name = out_file_h,
            input_file_name = 'shaders/src/*',
            shader_variation_definitions = shader_variation_definitions,
            shader_get_functions_h = shader_get_functions_h,
            shader_tables_h = shader_tables_h)
        outfile.write(outcode)
        outfile.close()

    # STEP 3: Create a gni file with the generated files.
    with open(out_file_gni, 'w') as outfile:
        outcode = template_shader_includes_gni.format(
            script_name = __file__,
            copyright_year = date.today().year,
            out_file_name = out_file_gni,
            input_file_name = 'shaders/src/*',
            shaders_list = ',\n'.join(['  "' + slash(shader) + '"' for shader in output_shaders]))
        outfile.write(outcode)
        outfile.close()


if __name__ == '__main__':
    sys.exit(main())
