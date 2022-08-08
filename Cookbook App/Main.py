from Website import create_app

app = create_app()

if __name__ == '__main__':   #Only if run this file, not input it
    app.run(debug=True)