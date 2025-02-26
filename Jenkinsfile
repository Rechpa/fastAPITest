pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'SonarQube'
        NEXUS_CREDENTIALS_ID = 'deploymentRepo'
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
        registry = "farahdiouani/fastapi-postgres-crud"
        registryCredential = 'docker-hub-credentials'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        IMAGE_NAME = "fastapi-postgres-crud"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out code...'
                    git branch: 'main',
                        url: 'https://github.com/Rechpa/fastAPITest.git'
                    echo 'Checkout completed.'
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh 'docker --version'
                    sh "docker build -t ${registry}:${IMAGE_TAG} . || exit 1"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Build and push finished successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
