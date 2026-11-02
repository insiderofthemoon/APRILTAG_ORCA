# APRILTAG ORCA

ROS 2 vision workspace for AUV ORCA, developed using Ubuntu 22.04 and ROS 2 Humble.

## Overview

This repository contains:
- AprilTag detection and decoding pipeline.
- QR Code detection and validation pipeline.
- Camera utilities.
- AprilTag marker assets and configuration.

## Repository Structure

```text
orca_ws/
├── apriltag_project/
│   ├── config/
│   ├── markers/
│   ├── scripts/
│   └── tag_mapping.yaml
├── qr_codes/
├── src/
│   ├── orca_apriltag/
│   └── orca_vision/
├── camera.py
├── README.md
└── .gitignore
ls -lh README.md
head -20 README.md
git status --short
## Development Notes

- All six AprilTag IDs have been tested.
- Camera calibration is needed for reliable pose estimation.
- Mission decision and vehicle-control integration are not included yet.
- Build artifacts (build/, install/, log/) are excluded from Git.

## Development Environment

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- AUV ORCA Vision Development
