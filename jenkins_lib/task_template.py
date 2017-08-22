# -*- coding: utf-8 -*-

def template_base_new(job_name, svn_url):
    template_base = u'''<flow-definition plugin="workflow-job@2.7"><actions/><description/><keepDependencies>false</keepDependencies><properties><org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty><triggers/></org.jenkinsci.plugins.workflow.job.properties.PipelineTriggersJobProperty></properties><definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.19"><script>node {
stage 'Checkout'   //从svn checkout脚本
checkout([$class: 'SubversionSCM', additionalCredentials: [], excludedCommitMessages: '', excludedRegions: '', excludedRevprop: '', excludedUsers: '', filterChangelog: false, ignoreDirPropChanges: false, includedRegions: '', locations: [[credentialsId: '42b62291-17a6-43f0-b09d-f9ba92869e05', depthOption: 'infinity', ignoreExternalsOption: true, local: '.', remote: '%s']], workspaceUpdater: [$class: 'UpdateUpdater']])

def mvnHome = tool 'master-maven'    //设置mvn的环境变量 
def javaHome = tool 'master-jdk-1.7'  //设置java的环境变量

stage 'Build'   //使用mvn编译脚本
sh "JAVA_HOME=$javaHome $mvnHome/bin/mvn clean install -U"
archiveArtifacts artifacts: '**/target/*.war', fingerprint: true  //设置fingerprint

stage 'copy patches'  //拷贝war包到指定目录
sh "ansible-playbook /opt/ansible-stage/site_stage1.yml -e 'target_hosts=%s'"

stage 'stop tomcat' //调用ansible脚本
sh "ansible-playbook /opt/ansible-stage/site_stage2.yml -e 'target_hosts=%s'"

stage 'backup' //调用ansible脚本
sh "ansible-playbook /opt/ansible-stage/site_stage3.yml -e 'target_hosts=%s'"

stage 'release patches' //调用ansible脚本
sh "ansible-playbook /opt/ansible-stage/site_stage4.yml -e 'target_hosts=%s'"

stage 'start tomcat' //调用ansible脚本
sh "ansible-playbook /opt/ansible-stage/site_stage5.yml -e 'target_hosts=%s'"

stage 'send email' //调用ansible脚本
sh "ansible-playbook /opt/ansible-stage/site_stage6.yml -e 'target_hosts=%s'"

}</script><sandbox>true</sandbox></definition><triggers/></flow-definition>''' % (svn_url, job_name, job_name, job_name, job_name, job_name, job_name)
    return template_base

