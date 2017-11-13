from flask import Flask, request, session, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def hello_world():

    return 'hello world!!'

@app.route('/main')
def main():

    return 'Main Page'

@app.route('/user/<username>')
def showUserProfile(username):

    app.logger.debug('RETRIEVE DATA - USER ID : %s' % username)
    app.logger.debug('RETRIEVE DATA - Check Complete')
    app.logger.warn('RETRIEVE DATA - Warning... User Not Found1')
    app.logger.error('RETRIEVE DATA - ERR! User unauthentification.')

    return 'USER : %s' % username

@app.route('/user/id/<int:userId>')
def showUserProfileById(userId):

    return 'USER ID : %d' % userId

@app.route('/account/login', methods=['POST'])
def login():

    if request.method == 'POST':
        userId = request.form['id']
        wp = request.form['wp']

        if len(userId) == 0 or len(wp) == 0:
            return userId + ', ' + wp + '로그인 정보를 제대로 입력하지 않았습니다.'

        session['logFlag'] = True
        session['userId'] = userId

        return session['userId'] + ' 님 환영합니다.'

    else:
        return 'Invalid access'

app.secret_key = 'sample_secret_key'

@app.route('/user', methods=['GET'])
def getUser():

    if session.get('logFlag') != True:
        return 'Invalid access'

    userId = session['userId']

    return '[GET][USER] USER ID : %s'.format(userId)

@app.route('/account/logout', methods=['POST', 'GET'])
def logout():

    session['logFlag'] = False
    session.pop('userId', None)

    return redirect(url_for('main'))

@app.errorhandler(400)
def uncaughtError(error):
    return '잘못된 사용입니다.'

if __name__ == '__main__':

    app.debug = True
    app.run()