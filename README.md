# DALT: Deep Activity Launching Test 
An activity-launching-test tool to generate intents as test cases that can reach deep
& extensive code statements in apps, which facilitates successfully launching activities, triggering crashes and identifying bugs, in a comprehensive manner.

## Structure:
- DALT
  - Apps: the 20 apps in the experiments
  - Instrumented_Apps: the exposed and instrumented apps in the experiments
  - Tool: DALT tools 
  - Experimental_Results
    - Manually_Examined_Paths
    - F-Droid_Summary: summaries of each app in F-Droid
    - Test_Execution: summaries of static analysis, generated test cases, and  execution logs
  
## Requirements:
* Install Java 1.8. Run "java -version" and "javac" to check whether it is successfully installed.
* Install Python 2.7. Run "python" to check whether it is successfully installed.
* Install the SMT solver, Z3, which requires the Z3 library and the dynamic link library for Java API.  
  * copy lib/libz3/libz3.so and lib/libz3/libz3java.so to [your\_library\_path]
  * add java.library.path into the enviroment variable file [enviroment_path], e.g., ~/.bash_profile, /etc/profile.
	   i.e., "export LD\_LIBRARY\_PATH=$LD\_LIBRARY\_PATH:[your\_library\_path]" to file [enviroment\_path].
  * save the modification (source [enviroment\_path])
* Android enviroment
  * Install Android sdk (usually includes tool Ant and ADB)
  * Install Ant
  * Install ADB
  * Run "ant -version" and "android create project" to check whether these tools are successfully configured
* Android device or emulator for test execution. Run "adb devices" to check whether the device is successfully connected to the computer 

## Usage of DALT tools:

* Preprocess: Exposing activities of the under-test app, and instrumenting the methods of the app for the method-coverage calculation.
  * Put the apk under test under the [apk_input_dir], and get the result in the [apk_output_dir].  
  * Run: python Tool/script/Prerocess.py [apk_input_dir] [apk_output_dir]  

* Test Generation: performing static analysis and generate test cases.
  * Run: python Tool/script/GenerateTestCases.py Tool/lib/dalt.jar [apk_input_dir] [testcase_dir] [execute_info_dir] [max_number_of_path]  
  * Get results in folder [testcase_dir].

* Activity Launching Test: test script to execute test cases
  * Run: python Tool/script/LaunchActs.py [testcase_dir]  [launch_dir] 
  * Get results in folder [launch_dir].

* Crash Collection 
  * python script/FindCrashes.py [testcase_dir]  [launch_dir]    

