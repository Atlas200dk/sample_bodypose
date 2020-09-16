# Body Pose Detection \(Python)

This application runs on Atlas 200 DK, to infer human body poses. The model used is modified from Lightweight OpenPose [Osokin, Daniil. "Real-time 2d multi-person pose estimation on CPU: Lightweight OpenPose." arXiv preprint arXiv:1811.12004 (2018)], an open-source pose detection network. This application can be run on various input formats, namely image input, video input as well as live camera input. 

The pose detection network originates from [Cao, Zhe, et al. "OpenPose: realtime multi-person 2D pose estimation using Part Affinity Fields." arXiv preprint arXiv:1812.08008 (2018)], where the network provides two outputs: heatmaps and PAF maps for each frame. In the post-processing of the model, both heatmaps and PAF maps are used to obtain multi-persion pose estimation. 

In this repository, the post-processing a simplied version for edge computing, where only the heatmap is used to calculate the predicted locations of the human body joints. A set of 14 detected joints are grouped, connected to form limbs and associated to a person. The diagram below represents connection scheme:

                     12                     12: head, 13: neck
                     |
                     |
               0-----13-----3
              /     / \      \
             1     /   \      4
            /     /     \      \
           2     6       9      5
                 |       |
                 7       10
                 |       |
                 8       11

    

The figure below shows the sample output on a single image input. The detected pose is displayed in the form of a skeleton overlay on the image.

**Figure**  OpenPose detection result<a name="zh-cn_topic_0228757088_fig64391558352"></a>  
    ![](figures/pose_detected.jpg "pose-detected")

## Software Preparation<a name="zh-cn_topic_0228757083_section17595135641"></a> 

Clone or download the project repository:

**mkdir -p $HOME/AscendProjects**
**cd $HOME/AscendProjects**  
**git clone ssh://git@rnd-gitlab-ca-g.huawei.com:2222/hispark/openpose-pythonc73.git**
OR
**wget https://rnd-gitlab-ca-g.huawei.com/hispark/openpose-pythonc73.git**   

Then, unzip the downloaded file:

**unzip openpose-pythonC73.zip**  

  
## Environment Preparation<a name="zh-cn_topic_0228757083_section17595135641"></a> 
Install required libraries for Python3 environment (OpenCV, PresentAgent and Python3env)
       
Please refer to https://github.com/Huawei-Ascend/samples/tree/master/common  
   

## Environment Deployment<a name="zh-cn_topic_0228757083_section1759513564117"></a>  

1.  Go to the root directory where the application code is located, such as: $HOME/AscendProjects/openpose-pythonC73/. 
     
    **cd $HOME/AscendProjects/openpose-pythonC73/** 

2.  Modify the configuration file.  

    Modify **presenter\_server\_ip** and **presenter\_view\_ip** in **script/body\_pose.conf** to the current ubuntu server and atlas200dk development board network port ip,           **presenter \_agent\_ip** is the ip of the network port connected to the ubuntu server on the development board.

    If you use USB connection, the USB network port ip of the development board is 192.168.1.2, and the network port ip of the virtual network card connected to the ubuntu server and the development board is 192.168.1.223, then the configuration file content is as follows:

    **presenter\_server\_ip=192.168.1.223**

    **presenter\_view\_ip=192.168.1.223**

    **presenter\_agent\_ip=192.168.1.2**

    
    Generally, when connecting via USB, atlas200dk\_board\_ip is the USB network port ip of the development board, and the default is 192.168.1.2. When connecting through a network port, atlas200dk\_board\_ip is the network port ip of the development board, and the default is 192.168.0.2.

3.  Copy the application code to the development board.
   
    Navigate to the root directory where the openpose-pythonC73 application code is located, such as: AscendProjects/openpose-pythonC73, execute the following command to copy the application code to the development board. If the copy fails, please check if there is a directory HIAI\_PROJECTS on the development board, and if not, create it.

    **scp -r ~/AscendProjects/openpose-pythonC73 HwHiAiUser@192.168.1.2:/home/HwHiAiUser/HIAI\_PROJECTS**

    Enter the development board password when prompted for password. The default password of the development board is **Mind@123**, as shown below:
<a name="zh-cn_topic_02287570831_zh-cn_topic_0198304761_fig1660453512014"></a>  

    ![](figures/files_copy.png)


    
4.  Start Presenter Server.

    **NOTE**: This step is required when the presenter server needs to be used for video or live display on the browser. Otherwise, skip this step.

    Execute the following command to start the Presenter Server in the background.

    **bash $HOME/AscendProjects/openpose-pythonC73/script/run_presenter_server.sh &**

    Log in to the Presenter Server using the prompted URL. The figure below shows that the Presenter Server has started successfully.

    **Figure**  Home Page Display<a name="zh-cn_topic_0228757088_fig64391558352"></a>  
![](figures/主页显示.png "Home page display")

    
    The communication between Presenter Server, Mind Studio and Atlas 200 DK is shown as below：


    **Figure**  Examples of IP addresses<a name="zh-cn_topic_0228757088_fig1881532172010"></a>  
![](figures/IP地址示例.png "Examples of IP addresses")

    NOTE:

    -   The IP address used by the Atlas 200 DK developer board is 192.168.1.2 (USB connection).
    -   The IP address for the communication between Presenter Server and Atlas 200 DK is the IP address of the UI Host server on the same network segment as Atlas 200 DK, for example: 192.168.1.223.
    -   This example of the IP address for accessing Presenter Server through a browser is 10.10.0.1. Since Presenter Server and Mind Studio are deployed on the same server, this IP address is also the IP for accessing Mind Studio through a browser.

    
5.  Copy acl.so to the development board. Please skip this step if it is already done in other projects.

    **scp ~/Ascend/ascend-toolkit/20.0.RC1/arm64-linux_gcc7.3.0/pyACL/python/site-packages/acl/acl.so HwHiAiUser@192.168.1.2:/home/HwHiAiUser/Ascend/**  

    **Please replace X.X.X with the actual version number of the Ascend-Toolkit development kit package**   
    **For example: the package name of the Toolkit package is Ascend-Toolkit-20.0.RC1-x86_64-linux_gcc7.3.0.run, then the version number of this Toolkit is 20.0.RC1.**


6. Log in to the development board and add environment variables. Please skip this step if it is already done in other projects.

    **ssh HwHiAiUser@192.168.1.2**  
    **vim ~/.bashrc**   
    Add two lines at the end    
    **export LD_LIBRARY_PATH=/home/HwHiAiUser/Ascend/acllib/lib64**   
    **export PYTHONPATH=/home/HwHiAiUser/Ascend/:\\${PYTHONPATH}**  
    ![](figures/bashrc.png)   

    Execute the following command to make the environment variable take effect
    **source ~/.bashrc**  


## Running the Application
1. Check whether the "CAMERA0" camera is used.
   The "CAMERA0" camera is used by default in the code. Please refer to the link below for the viewing method.   
   https://support.huaweicloud.com/usermanual-A200dk_3000/atlas200dk_02_0051.html 

2. Log in to the development board. Navigate to the code directory corresponding to the required input source format (image, video or live camera), and execute one of the following commands to run the application according to the input source format. 

    **NOTE**: To execute it, you could use the default input (just run **python3 main.py** without parameter), or input parameters as below for input/output paths and model path as indicated in **main.py**. For the video input, you also have the option to save the output as a video or display to presenter server, with the value in parameter 'is_presenter_server' set to False or True, respectively .

    *Image input source*: 

    **cd ~/HIAI_PROJECTS/openpose-pythonC73/code_image**   
    **python3 main.py --model='model/body_pose.om' --frames_input_src='tennis_player.jpg' --output_dir='outputs'**

    *Video input source (output video)*:

    **cd ~/HIAI_PROJECTS/openpose-pythonC73/code_video**   
    **python3 main.py --model='model/body_pose.om' --frames_input_src='yoga.mp4' --output_dir='outputs' --is_presenter_server=False**

    Video input source (output streamed to presenter server)*:

    **cd ~/HIAI_PROJECTS/openpose-pythonC73/code_video**   
    **python3 main.py --model='model/body_pose.om' --frames_input_src='yoga.mp4' --output_dir='outputs' --is_presenter_server=True**

    *Live camera source*:

    **cd ~/HIAI_PROJECTS/openpose-pythonC73/code_live**   
    **python3 main.py --model='model/body_pose.om'**

3.  If you need to view the detection results using presenter server for the live input or video source, log in to the Presenter Server website using the URL that was prompted when the Presenter Server service was started. Otherwise, skip this step.

Wait for the Presenter Agent to transmit data to the server, and click "Refresh" to refresh. When there is data, the status of the corresponding Channel turns green, as shown in the figure below.

**Figure**  Presenter Server<a name="zh-cn_topic_0228461904_zh-cn_topic_0203223294_fig113691556202312"></a>  
![](figures/presenter.png "Presenter-Server-interface") 

Click the corresponding View Name link on the right, such as "video" in the above picture, to view the results.

## Stopping Application<a name="zh-cn_topic_0228757088_section1092612277429"></a>

If the presenter server is being used for display, stop 

-   **Stop Presenter Server**

    The Presenter Server service will always be running after it is started. If you want to stop the Presenter Server service corresponding to the pose detection application, you can perform the following operations.

    Execute the following command on the command line on the server where the process of the Presenter Server service is running:
    
    **ps -ef | grep presenter**

    ```
    ascend@ubuntu:~/AscendProjects/openpose-pythonC73/script$ ps -ef | grep presenter
    ascend 9560 1342 0 02:19 pts/4  00:00:04   python3/home/ascend/AscendProjects/openpose-pythonC73.bak/script/..//present
    erserver/presenter_server.py --app openpose-pythonC73
    ```

    As shown above, _9650_ is the process ID of the Presenter Server service corresponding to the openpose-pythonC73 application.

    If you want to stop this service, execute the following command:


    **kill -9** _9650_
