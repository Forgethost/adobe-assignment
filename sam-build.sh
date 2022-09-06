echo "Entered sam build phase. .."
echo 'CODEBUILD _BUILD _SUCCEEDING' ${CODEBUILD_BUILD_SUCCEEDING}
if [ ${CODEBUILD_BUILD_SUCCEEDING} -eq 1 ]
  then
    sam build --tenplate ./cloudformation/template.yaml --config-file ./cloudformation/sanconfig.toml
  else
    exit 1
