pipeline {
    agent any


    environment {
        SONARQUBE_ENV = 'SonarQube'  // SonarQube environment name
        NEXUS_CREDENTIALS_ID = 'deploymentRepo'  // Nexus credentials ID in Jenkins
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
        RELEASE_VERSION = "1.0"
        registry = "farahdiouani/gestion-station-ski"
        registryCredential = 'docker-hub-credentials'
        IMAGE_TAG = "${RELEASE_VERSION}-${env.BUILD_NUMBER}"
        IMAGE_NAME = "fastapi-postgres-crud"
    }


    stages {
            stage('Checkout') {
                steps {
                    git branch: 'main',
                    url: 'https://github.com/Rechpa/fastAPITest.git';
                }
            }

              stage('Build Image') {
            steps {
                echo 'Building Docker Image...'
                script {
                    dockerImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                    echo "Docker image built: ${dockerImage.imageName()}"
                }
                echo 'Docker Build Image stage completed.'
            }
        }
             
                 }

                 post {
                     success {
                         echo 'Build finished successfully!'
                     }
                     failure {
                         echo 'Build failed!'
                     }
                 }


}