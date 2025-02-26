pipeline {
    agent any
    stages {
            stage('Checkout') {
                steps {
                    git branch: 'master',
                    url: 'https://github.com/Rechpa/fastAPITest.git';
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