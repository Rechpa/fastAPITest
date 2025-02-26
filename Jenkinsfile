pipeline {
    agent any

    environment {
        registry = "farahdiouani/fastapi-postgres-crud"
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Use Jenkins build number as tag
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')

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
                    sh "docker build -t ${registry}:${IMAGE_TAG} ." // Uses dynamic build number
                    sh "docker tag ${registry}:${IMAGE_TAG} ${registry}:latest" // Also tag as latest
                    echo "Docker image built: ${registry}:${IMAGE_TAG}"
                }
            }
        }

        stage('Login to Docker') {
            steps {
                echo 'Logging to DockerHub...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                        echo 'DockerHub login successful.'
                    }
                }
                echo 'Login to DockerHub stage completed.'
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    echo 'Pushing Docker image to DockerHub...'
                    sh "docker push ${registry}:${IMAGE_TAG}"
                    sh "docker push ${registry}:latest"
                    echo "Docker image pushed: ${registry}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        success {
            echo 'Docker build and push completed successfully!'
        }
        failure {
            echo 'Docker build failed!'
        }
    }
}
