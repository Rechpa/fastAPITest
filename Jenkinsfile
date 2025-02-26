pipeline {
    agent {
        kubernetes {
            cloud 'kubernetes' // Using your defined Kubernetes cloud
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: jenkins-agent
spec:
  containers:
    - name: docker
      image: docker:latest
      command: ['cat']
      tty: true
      volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
    - name: kubectl
      image: bitnami/kubectl:latest
      command: ['cat']
      tty: true
    - name: helm
      image: alpine/helm:latest
      command: ['cat']
      tty: true
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
"""
        }
    }

    environment {
        registry = "farahdiouani/fastapi-postgres-crud"
        IMAGE_TAG = "${env.BUILD_NUMBER}" // Jenkins build number as tag
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
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
                container('docker') {
                    script {
                        echo 'Building Docker Image...'
                        sh "docker build -t ${registry}:${IMAGE_TAG} ." 
                        sh "docker tag ${registry}:${IMAGE_TAG} ${registry}:latest"
                        echo "Docker image built: ${registry}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Login to Docker') {
            steps {
                container('docker') {
                    script {
                        withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                            sh "docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD"
                            echo 'DockerHub login successful.'
                        }
                    }
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                container('docker') {
                    script {
                        echo 'Pushing Docker image to DockerHub...'
                        sh "docker push ${registry}:${IMAGE_TAG}"
                        sh "docker push ${registry}:latest"
                        echo "Docker image pushed: ${registry}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                container('helm') {
                    script {
                        echo 'Deploying with Helm...'
                        withCredentials([file(credentialsId: 'mykubeconfig', variable: 'KUBECONFIG')]) {
                            sh """
                            export KUBECONFIG=${KUBECONFIG}
                            helm upgrade --install fastapi2 fastapi-helm \
                                --set image.repository=${registry} \
                                --set image.tag=${IMAGE_TAG}
                            """
                        }
                        echo 'Helm deployment completed.'
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
