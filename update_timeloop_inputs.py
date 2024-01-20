import os
import sys
import glob
import re

CHANGES = [
    "linear_pruned",
    "problem_space_files",
    "log_stats",
    "tile_width",
    "log_interval",
    "CNN_Layer",
    "ordered_accesses",
    "router_energy",
    "tree_like",
    "arch_space_files",
    "log_oaves",
    "penalize_consecutive_bypass_fails",
    "emit_whoop_nest",
    "condition_on",
    "energy_per_hop",
    "max_permutations_per_if_visit",
    "gate_on_zero_operand",
    "gcc_ar",
    "num_ports",
    "multiple_buffering",
    "timeloop_mapper",
    "cluster_area",
    "outer_to_inner",
    "spatial_skip",
    "log_all",
    "wire_energy",
    "metadata_word_bits",
    "optimization_metric",
    "word_bits",
    "action_optimization",
    "cnn_layer",
    "spatial_skip",
    "num_threads",
    "arch_space_sweep",
    "live_status",
    "step_size",
    "min_utilization",
    "network_type",
    "block_size",
    "sync_interval",
    "log_suboptimal",
    "representation_format",
    "flattened_rankIDs",
    "gemm_ABZ",
    "arch_spec",
    "last_level_accesses",
    "optimization_metrics",
    "inner_to_outer",
    "compression_rate",
    "filter_revisits",
    "vector_access_energy",
    "rank_application_order",
    "log_oaves_mappings",
    "read_write",
    "fixed_structured",
    "gcc_ranlib",
    "adder_energy",
    "timeloop_model",
    "search_size",
    "victory_condition",
    "random_pruned",
    "access_X",
    "skipping_spatial",
    "payload_word_bits",
    "num_banks",
    "addr_gen_energy",
    "cluster_size",
    "compute_optimization",
    "network_word_bits",
    "data_spaces",
    "timeloop_metric",
    "timeloop_metrics",
    "timeloop_simple_mapper",
    "timeloop_design_space",
    "timeloop_unit_tests",
]

FILE_NAME_CHANGES = [
    "timeloop_model.py",
    "timeloop_mapper.py",
]


def recursive_find_files(path, targets):
    # Change this to glob.glob() if you want to use wildcards
    files = []
    for t in targets:
        found = glob.glob(os.path.join(path, t))
        files.extend([f for f in found if os.path.isfile(f)])
    for d in os.listdir(path):
        if os.path.isdir(os.path.join(path, d)) and ".git" not in d:
            files.extend(recursive_find_files(os.path.join(path, d), targets))
    return files


def replace_in_file(file, changes, write=False):
    lines = open(file).readlines()
    changed_lines = []
    for i, l in enumerate(lines):
        for v in changes:
            regex = r"(?<!-)\b{}\b(?!-)(?!\.hpp)(?!\.cpp)".format(v.replace("_", "-"))
            lines[i] = re.sub(regex, v, lines[i])
        if l != lines[i]:
            changed_lines.append((i, l, lines[i]))
    if write:
        open(file, "w").write("".join(lines))
    return changed_lines


def replace_in_file_name(file, changes, write=False):
    new_file = file
    for v in changes:
        regex = r"(?<!-)\b{}\b(?!-)".format(v.replace("_", "-"))
        new_file = re.sub(regex, v, new_file)
    if write:
        os.rename(file, new_file)
    return new_file


if __name__ == "__main__":
    start_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    FILE_TARGETS = [
        "*.py",
        "*.yaml",
        "*.cpp",
        "*.hpp",
        "*.cfg",
        "*.txt",
        "*SConscript",
        "*.h",
        "*.c",
        "*.sh",
        "*.md",
        "*.rst",
        "*.json",
        "*.xml",
        "*.in",
        "*.cmake",
    ]
    files = list(recursive_find_files(start_dir, FILE_TARGETS))
    files_with_changes = [f for f in files if replace_in_file(f, CHANGES)]
    files_with_name_changes = [
        f for f in files if replace_in_file_name(f, FILE_NAME_CHANGES) != f
    ]

    def fullpath(x):
        return os.path.abspath(os.path.realpath(os.path.expanduser(x)))

    this_script_path = fullpath(__file__)
    files = [fullpath(f) for f in files]
    files = [
        f
        for f in files
        if os.path.isfile(f) and not os.path.samefile(f, this_script_path)
    ]

    for f in files_with_changes:
        n_changes = len(replace_in_file(f, CHANGES))
        print(f"Found file {f} with {n_changes} changes")
        print(
            "\n".join(
                [
                    f"{i}\t: {l.strip()} -> {nl.strip()}"
                    for i, l, nl in replace_in_file(f, CHANGES)
                ]
            )
        )
    for f in files_with_name_changes:
        print(
            f"Found file {f} with name change to {replace_in_file_name(f, FILE_NAME_CHANGES)}"
        )

    print(
        f"Found {len(files_with_changes) + len(files_with_name_changes)} files with changes."
    )
    print(f'If you want to write changes, enter "YES": ')
    if input() == "YES":
        for f in files_with_changes:
            replace_in_file(f, CHANGES, write=True)
        for f in files_with_name_changes:
            replace_in_file_name(f, FILE_NAME_CHANGES, write=True)
        print("Changes written")
    else:
        print(f"Aborted. No changes written.")
