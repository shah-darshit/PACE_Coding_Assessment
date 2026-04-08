import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


#defining the clone funtion for each repo
def clone_repo(repo_str, dest):
    org_repo, branch = repo_str.split(':')
    url = f"https://github.com/{org_repo}.git"
    repo_name = org_repo.split('/')[1]
    target = os.path.join(dest, repo_name)

    result = subprocess.run(
        ['git', 'clone', '-b', branch, url, target],
        capture_output= True,
        text=True
    )

    if result.returncode !=0:
        print(f"Skipping {repo_str} : Error - {result.stderr.strip()}")
    else:
        print(f"Cloned {repo_str}.")

# main loop for parsing through arguements and setting up futures in queue
def main():
    parser  = argparse.ArgumentParser()
    parser.add_argument('--repos', nargs='+', required=True)
    parser.add_argument('--dest', required=True)
    parser.add_argument('--ntasks', type=int, required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.dest):
        raise FileNotFoundError(f"Destination directory '{args.dest}' does not exist")

    if args.ntasks < 1:
        raise ValueError("--ntasks must be >= 1")

    #setting up futures in queues given the number of workers
    with ThreadPoolExecutor(max_workers=args.ntasks) as executor:
        futures = {
            executor.submit(clone_repo, repo, args.dest): repo
            for repo in args.repos
        }
        for future in as_completed(futures):
            repo = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Failed {repo}: {e}")


if __name__ == '__main__':
    main()
