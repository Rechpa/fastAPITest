pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'SonarQube'
        NEXUS_CREDENTIALS_ID = 'deploymentRepo'
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
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

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh 'docker build -t fastapi-postgres-crud:5 .'
                }
            }
        }
    }

    post {
        success {
            echo 'Docker build completed successfully!'
        }
        failure {
            echo 'Docker build failed!'
        }
    }
}
