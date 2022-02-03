# Dataset Converter
To manipulate and convert datasets to our format to use with Monitor Sample of https://github.com/nokiatech/omaf.
There are two types of converters;
- The Hamilton Quaternion to Euler Angles
- Gaze and Head motion dataset to Euler Angles and separate gaze data


## From the unit Hamilton Quaternion to Euler Angles Converter
Convert Head Motions from the Hamilton Quaternion to Euler Angles.
360-Degree Video Head Movement Dataset: https://dl.acm.org/do/10.1145/3193701

### Usage
Place results folder to the project root. The output will be written to heads folder.
Format;
- quaternion-to-euler
  - converter.py
  - results
    - uid_id
      - test_id
        - VideoName
          - HeadMotionLogs.txt
  - heads
    - VideoName_uid

### Output
There are head motions for different videos. 
Format: videoName_userID 
Example: diving_0, diving_1, etc

Note that some users did not test some videos.
So, some head motion files can be missing.
For instance;
rhino_0, rhino_3, rhino_5, rhino_8, ...
rhino_2, rhino_4, rhino_5, rhino_6, rhino_7, ... are missing
