#!/bin/bash
#SBATCH --job-name=elastic_batch
#SBATCH --account=def-teseo
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --array=0-99
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err

set -e

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OPENBLAS_NUM_THREADS=$SLURM_CPUS_PER_TASK

module load python/3.12.4
source /home/teseo/scratch/polyfem-env/bin/activate

mkdir -p logs

python run_mesh_batch.py all_meshes.txt