#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

MEM_LIMIT="30g"

rm -rf $SCRIPTPATH/output && mkdir -p $SCRIPTPATH/output && chmod 777 $SCRIPTPATH/output

# Same restrictions as on Grand Challenge
docker run --rm \
        --gpus=all \
        --memory="${MEM_LIMIT}" \
        --memory-swap="${MEM_LIMIT}" \
        --network="none" \
        --cap-drop="ALL" \
        --security-opt="no-new-privileges" \
        --shm-size="128m" \
        --pids-limit="256" \
        -v $SCRIPTPATH/test:/input:ro \
        -v $SCRIPTPATH/output:/output \
        mama_synth_algorithm

if [ -f $SCRIPTPATH/output/images/synthetic-contrast-dce-mri-slice-breast/output.mha ]; then
    echo "Tests successfully passed..."
else
    echo "Expected output was not found..."
fi
