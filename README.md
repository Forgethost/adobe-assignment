# adobe-assignment
Adobe Technical Evaluation Assignment repository

## Prerequisites
-   _python 3.8_ installed in local machine
-   _sam cli_ installed in local machine
-   clone repo from _github_
-   AWS account user with AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY set in local machine having admin access
-   _S3 bucket_ for input/output file storage
###Direct Deployment of application
We are using AWS SAM for packaging serverless application and deployment to AWS
*   Package application using sam cli  
Navigate to application **_cloudformation_** directory in command prompt/cli, issue **sam build** command  
    ```sam build --config-env dev  ```  
-   Deploy application using sam  
```sam deploy --config-env dev  ```  
    
###Application deployment using CI/CD pipeline  
We are using S3 as source repo provide
*   Zip application repo in a directory  
Navigate to application **_root_** directory in terminal and issue **rm** and **zip** commands  
    >```rm -rf <your-staging-directory in local machine>/adobe-assignment.zip ```  
      
    >```zip -r <your-staging-directory in local machine>/adobe-assignment.zip . -x ./cloudformation/.aws-sam\* ./.tox/**\* ./test-reports/**\* ./tests/__pycache__\* ./__pycache__\*```
-   Copy application to s3 using **_aws cli_** command  
```aws cloudformation create-change-set --stack-name skp-app-ppl-stack --change-set-name skp-app-ppl-manual-create --template-body file://template.yaml --change-set-type UPDATE --capabilities CAPABILITY_ NAMED_IAM --parameters file://parameters.json  ```  
  
###CI/CD pipeline infrastructure Deployment
We are using cloudformation template to deploy _codepipeline_ and _codebuild_ infrastructure to AWS
*   CI/CD infrastructure deployment using cloudformation  
Navigate to application **_codepipeline_** directory in command prompt/cli, issue **aws cloudformation** command  
    ```aws cloudformation create-change-set --stack-name skp-app-ppl-stack --change-set-name skp-app-ppl-manual-create --template-body file://template.yaml --change-set-type CREATE --capabilities CAPABILITY_ NAMED_IAM --parameters file://parameters.json```  
> Incase unt to upgrade codepipeline stack after any changes to codepipeline CFN template  
```aws cloudformation create-change-set --stack-name skp-app-ppl-stack --change-set-name skp-app-ppl-manual-create --template-body file://template.yaml --change-set-type UPDATE --capabilities CAPABILITY_ NAMED_IAM --parameters file://parameters.json  ```  

###Execution of application
We are using AWS SAM for packaging serverless application and deployment to AWS
*   From console    
    -   Navigate to lambda that starts with  **skp-app**
    -   Create test event with any json input and execute lambda  
> The input file S3 bucket and prefix is parameterized as environment variables in _cloudformation/samconfig.toml_  
> To **override** this information with your own bucket name and prefix that containes the input file  
> _Input file name_ is also parameterized in _cloudformation/samconfig.toml_, please **change** as needed  
>   
>   The output file S3 bucket and prefix is parameterized as environment variables in _cloudformation/samconfig.toml_
> To **override** this information with your own bucket name and prefix where the output file is desired to be stored

![Alt text](.img/Flowcharts.png?raw=true "Flowchart")


