pipeline {
    agent any

    environment {
        registry = "farahdiouani/fastapi-postgres-crud"
        IMAGE_TAG = "${env.BUILD_NUMBER}" 
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
        KUBE_CONFIG = credentials('mykubeconfig') // Kubernetes credentials
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out code...'
                    git branch: 'main', url: 'https://github.com/Rechpa/fastAPITest.git'
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

        /* 
        stage('Deploy with Helm') {
            steps {
                script {
                    echo 'Deploying with Helm...'
                    withCredentials([file(credentialsId: 'mykubeconfig', variable: 'KUBECONFIG')]) {
                        sh "helm upgrade -i fastapi2 fastapi-helm"
                    }
                    echo 'Helm deployment completed.'
                }
            }
        } 
        */
        stage('Prepare Environment') {
    steps {
        script {
            sh 'rm -rf FastAPIArgo'  // Delete the previous clone
        }
    }
}



        stage('Update Config Repo') {
    steps {
        script {
            echo 'Cloning the configuration repository...'
            sh 'git clone https://gitlab.com/Rechpa/FastAPIArgo.git'
            dir('FastAPIArgo') {
                sh "git config user.email 'farahdiouani3@gmail.com'"
                sh "git config user.name 'rechpa'"

                echo 'Updating deployment manifest...'
                sh "sed -i 's|image: farahdiouani/fastapi-postgres-crud:.*|image: farahdiouani/fastapi-postgres-crud:${IMAGE_TAG}|' fastapi-deployment.yaml"

                echo 'Committing and pushing changes...'
                sh 'git add .'
                sh 'git commit -m "Update image to ${IMAGE_TAG}"'
                sh 'git push https://rechpa:eyladata2025@gitlab.com/Rechpa/FastAPIArgo.git'
            }
        }
    }
}

    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed!'
        }
    }
}
