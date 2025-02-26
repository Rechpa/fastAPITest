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
                    sh "docker build -t ${registry}:${IMAGE_TAG} ."
                    sh "docker tag ${registry}:${IMAGE_TAG} ${registry}:latest"
                    echo "Docker image built: ${registry}:${IMAGE_TAG}"
                }
            }
        }

        stage('Login to Docker') {
            steps {
                script {
                    echo 'Logging into DockerHub...'
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                        echo 'DockerHub login successful.'
                    }
                }
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

        stage('Deploy with Helm') {
            steps {
                script {
                    echo 'Deploying with Helm...'

                    // Fix: Escape $ sign correctly
                    def helmList = sh(script: "helm list -q | grep '^fastapi2\\$'", returnStatus: true)

                    if (helmList == 0) {
                        echo "Helm release exists. Upgrading..."
                        sh "helm upgrade fastapi2 fastapi-helm"
                    } else {
                        echo "Helm release does not exist. Installing..."
                        sh "helm install fastapi2 fastapi-helm"
                    }

                    echo 'Helm deployment completed.'
                }
            }
        }
    }

    post {
        success {
            echo 'Docker build, push, and Helm deployment completed successfully!'
        }
        failure {
            echo 'Pipeline execution failed!'
        }
    }
}
