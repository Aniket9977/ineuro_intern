from app.main import app
import os
if __name__ == '__main__':
    # Make sure uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
