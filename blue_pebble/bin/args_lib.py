import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpus',    '-c', type=int, nargs='?', default=1)
    parser.add_argument('--gpus',    '-g', type=int, nargs='?')
    parser.add_argument('--days',    '-d', type=int, nargs='?', default=0, help="time in days")
    parser.add_argument('--hours',   '-t', type=int, nargs='?', default=23, help="time in hours")
    parser.add_argument('--mins',          type=int, nargs='?', default=0, help="time in mins")
    parser.add_argument('--memory',  '-m', type=int, nargs='?',             help="memory in gp")
    parser.add_argument('--queue',         type=str, nargs='?',             help="queue")
    parser.add_argument('--gputype',       type=str, nargs='?',             choices=["GTX1080", "RTX2080", "RTX2080Ti", "RTX3090"], help="{GTX1080, RTX2080, RTX2080Ti, RTX3090}")
    parser.add_argument('--venv',          type=str, nargs='?')
    parser.add_argument('--condaenv',      type=str, nargs='?')
    parser.add_argument('--module-list',   type=str, nargs='?')
    parser.add_argument('--workdir',       type=str, nargs='?', default='$SLURM_SUBMIT_DIR')
    parser.add_argument('--jobname',      type=str, help="use a friendly name for the job output")
    parser.add_argument('--autoname', action='store_true',                   help="extract output filename based on job --- assumes uses third argument of cmd, as in python file.py output_filename")
    parser.add_argument('--port',          type=str, nargs='*', help="ports to ssh tunnel back to login nodes")
    parser.add_argument('cmd',           type=str, nargs='*',             help="job command --- must be last argument")

    args = parser.parse_args()
    args.cmd = ' '.join(args.cmd)

    if args.autoname:
        args.jobname = args.cmd.split(' ')[2]

    return args

def get_slurm_opts(args=None):
    if args is None:
        args = get_args()

    options = {}

    options["time"] = f"{args.days}-{str(args.hours).zfill(2)}:{str(args.mins).zfill(2)}:00"
    options["nodes"] = f"1"
    options["ntasks-per-node"] = f"{args.cpus}"

    if args.memory is not None:
        options["mem"] = f"{args.memory}gb"

    if args.gpus:
        gpu_specs=["gpu"]
        if args.gputype:
            gpu_specs.append(args.gputype)
        gpu_specs.append(str(args.gpus))

        options["gres"] = ":".join(gpu_specs)

    if args.queue is not None:
        options["partition"] = f"{args.queue}"

    if args.jobname is not None:
        options["job-name"] = f"{args.jobname}"

    return options
