import os
import argparse
import inference


def batch():
    parser = argparse.ArgumentParser(description="Wrapper script for COSeg Inference")
    parser.add_argument("query", default="working_dir/input", help="Path to query directory")

    parser.add_argument("--type", default="ply", help="Query file type: ply, npy or blocks")
    parser.add_argument("--support", default="data/support", help="Path to support data")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate the result and save metrics")

    parser.add_argument("--cfg", default="config/s3dis_COSeg_fs.yaml", help="Path to configuration file")
    parser.add_argument("--weight", default="data/weight/s31_1w5s.pth", help="Path to model weight file")
    parser.add_argument("--voxel-size", type=float, default=0.02, help="Voxel size parameter, the lower the finer")
    batch_args = parser.parse_args()

    batch_query_path = batch_args.query
    file_type = batch_args.type

    if not os.path.exists(batch_query_path):
        raise ValueError(f"Query path {batch_query_path} does not exist.")

    batch_query_list = os.listdir(batch_query_path)
    if file_type == "ply":
        batch_query_list = [f for f in batch_query_list if f.endswith(".ply")]
    elif file_type == "npy":
        batch_query_list = [f for f in batch_query_list if f.endswith(".npy")]
    elif file_type == "blocks":
        batch_query_list = [f for f in batch_query_list if os.path.isdir(os.path.join(batch_query_path, f))]
    else:
        raise ValueError(f"Unsupported query file type: {file_type}, please use ply, npy or blocks.")

    count = len(batch_query_list)

    # sort the queries by name
    batch_query_list.sort()

    print(f"\nBatch inference started, total {count}: {batch_query_list}")

    for i, query in enumerate(batch_query_list):

        print(f"\n---Current: {query} ({i + 1}/{count})---")
        batch_args.query = os.path.join(batch_query_path, query)
        batch_args.vis_progress = False
        batch_args.vis_result = False
        inference.main(batch_args)
    print("Batch inference completed, total", count, "queries.")


if __name__ == "__main__":
    batch()
