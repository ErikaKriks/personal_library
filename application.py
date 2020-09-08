import ast
from tempfile import mkdtemp

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///books.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # rodyti pasirinkto list'o knygas
        list_type = request.form.get("listname")
        print('INDEX | list type: ' + str(list_type), flush=True)

        check_type = request.form.get("check_value")
        print('INDEX | check: ' + str(check_type), flush=True)

        books = db.execute("""SELECT * FROM books WHERE user_id = :id
                            AND started IS NOT NULL AND finished IS NULL ORDER BY author""",
                           id=session["user_id"])

        # by default show all books
        lists = db.execute("""SELECT * FROM books WHERE user_id = :id ORDER BY author""",
                           id=session["user_id"])

        # only lent out books
        if str(check_type) == "True":
            if str(list_type) == "all":
                # show all the books
                lists = db.execute("""SELECT * FROM books WHERE user_id = :id AND lent = true ORDER BY author""",
                                        id=session["user_id"])

            elif str(list_type) == "lent":
                # show lent books
                lists = db.execute("""SELECT * FROM books WHERE user_id = :id AND lent = true ORDER BY author""",
                                        id=session["user_id"])

            elif str(list_type) == "notmine":
                # show borrowed books
                lists = db.execute("""SELECT * FROM books WHERE owner != :owner OR owner IS NULL AND user_id = :id AND lent = true ORDER BY author""",
                                        id=session["user_id"],
                                        owner="personal")

            elif str(list_type) == "read":
                # show read books
                lists = db.execute("""SELECT * FROM books WHERE user_id = :id AND finished IS NOT NULL AND lent = true ORDER BY author""",
                                        id=session["user_id"])

            elif str(list_type) == "personal":
                # show personal books
                lists = db.execute("""SELECT * FROM books WHERE owner = :owner AND user_id = :id AND lent = true ORDER BY author""",
                                        id=session["user_id"],
                                        owner="personal")
            
        else:
            if str(list_type) == "all":
                # show all the books
                lists = db.execute("""SELECT * FROM books WHERE user_id = :id ORDER BY author""",
                                        id=session["user_id"])

            elif str(list_type) == "lent":
                lists = db.execute("""SELECT * FROM books WHERE user_id = :id AND lent = true ORDER BY author""",
                                        id=session["user_id"])

            elif str(list_type) == "notmine":
                # show borrowed books
                lists = db.execute("""SELECT * FROM books WHERE owner != :owner OR owner IS NULL AND user_id = :id ORDER BY author""",
                                        id=session["user_id"],
                                        owner="personal")

            elif str(list_type) == "read":
                # show read books
                lists = db.execute("""SELECT * FROM books WHERE user_id = :id AND finished IS NOT NULL ORDER BY author""",
                                        id=session["user_id"])

            elif str(list_type) == "personal":
                # show personal books
                lists = db.execute("""SELECT * FROM books WHERE owner = :owner AND user_id = :id ORDER BY author""",
                                        id=session["user_id"],
                                        owner="personal")

        return render_template("index.html", books=books, lists=lists)

    # else:
    if request.method == "GET":
        # presents currently reading books

        books = db.execute("""SELECT * FROM books WHERE user_id = :id
                            AND started IS NOT NULL AND finished IS NULL ORDER BY author""",
                           id=session["user_id"])

        lists = db.execute("""SELECT * FROM books WHERE user_id = :id ORDER BY author""",
                           id=session["user_id"])

        # print(lists)

        return render_template("index.html", books=books, lists=lists)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        hashed = generate_password_hash(request.form.get("password"))
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # USERNAME CHECK
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username does not exist
        if len(rows) != 0:
            return apology("this username is taken", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        elif not confirmation:
            return apology("must confirm password", 403)

        # Ensure confirmation password matches password
        elif not password == confirmation:
            return apology("passwords do not match", 403)

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hashed)

        # Log user in
        session["user_id"] = id
        session["username"] = username

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/new-book", methods=["GET", "POST"])
@login_required
def new_book():
    if request.method == "POST":
        author = request.form.get("author").title()  # capitalize first leter of every word
        print('NEW BOOK | author: ' + str(author), flush=True)
        title = request.form.get("title").capitalize()  # capitalize first letter
        print('NEW BOOK | title: ' + str(title), flush=True)
        isbn = request.form.get("ISBN")
        print('NEW BOOK | isbn: ' + str(isbn), flush=True)
        page_count = request.form.get("page_count")
        print('NEW BOOK | page_count: ' + str(page_count), flush=True)
        genre = request.form.get("genre")
        print('NEW BOOK | genre: ' + str(genre), flush=True)
        notes = request.form.get("notes")
        print('NEW BOOK | notes: ' + str(notes), flush=True)
        belonging_check = request.form.get("belongingCheck")
        print('NEW BOOK | belongingCheck: ' + str(belonging_check), flush=True)
        start_date = request.form.get("start_date")
        print('NEW BOOK | start_date: ' + str(start_date), flush=True)
        finish_date = request.form.get("finish_date")
        print('NEW BOOK | finish_date: ' + str(finish_date), flush=True)
        ratings = request.form.get("ratings")
        print('NEW BOOK | ratings: ' + str(ratings), flush=True)
        date_reading_now = request.form.get("dateReadingNow")
        print('NEW BOOK | dateReadingNow: ' + str(date_reading_now), flush=True)

        if not date_reading_now:
            db.execute(
                "INSERT INTO books "
                "(user_id, title, author, pages, isbn, genre, rating, started, finished, owner, notes) "
                "VALUES "
                "(:user_id, :title, :author, :pages, :isbn, :genre, :rating, :started, :finished, :owner, :notes)",
                user_id=session["user_id"],
                title=title,
                author=author,
                pages=page_count,
                isbn=isbn,
                genre=genre,
                rating=ratings,
                started=start_date,
                finished=finish_date,
                owner=belonging_check,
                notes=notes)

            return redirect("/")

        else:
            db.execute(
                "INSERT INTO books "
                "(user_id, title, author, pages, isbn, genre, rating, started, owner, notes) "
                "VALUES "
                "(:user_id, :title, :author, :pages, :isbn, :genre, :rating, :started, :owner, :notes)",
                user_id=session["user_id"],
                title=title,
                author=author,
                pages=page_count,
                isbn=isbn,
                genre=genre,
                rating=ratings,
                started=date_reading_now,
                owner=belonging_check,
                notes=notes)

            return redirect("/")

    else:
        return render_template("new-book.html")


@app.route("/quotes", methods=["GET", "POST"])
@login_required
def quotes():
    # presents quotes if there are any

    if request.method == "GET":
        # query database for data about quotes
        quotes_result = db.execute("""SELECT * FROM quotes
                            JOIN books ON books.book_id = quotes.book_id
                            WHERE quotes.user_id = :user_id""",
                                   user_id=session["user_id"])

        # query database for data about books
        books_result_author = db.execute(
            "SELECT author FROM books WHERE user_id = :id ORDER BY author COLLATE NOCASE ASC",
            id=session["user_id"])
        print('QUOTES | books_result_author: ' + str(books_result_author), flush=True)

        books_result_title = db.execute("SELECT title FROM books WHERE user_id = :id ORDER BY title COLLATE NOCASE ASC",
                                        id=session["user_id"])
        print('QUOTES | books_result_title: ' + str(books_result_title), flush=True)

        # if there are no books in database
        if books_result_author == 0:
            return apology("You need to add a book first!")

        if books_result_title == 0:
            return apology("You need to add a book first!")

        return render_template("quotes.html", quotes=quotes_result, books_author=books_result_author,
                               books_title=books_result_title)

    else:
        quote = request.form.get("quote")
        author = request.form.get("author")
        book_title = request.form.get("book_title")

        if not quote:
            return apology("type your quote!", 404)

        if not author:
            return apology("select an author", 404)

        if not book_title:
            return apology("select the book ", 404)

        books_result = db.execute("""SELECT book_id FROM books WHERE title = :title AND user_id = :user_id""",
                                  title=book_title,
                                  user_id=session["user_id"])

        # inserting new data into database
        db.execute("INSERT INTO quotes (user_id, book_id, quote) VALUES (:user_id, :book_id, :quote)",
                   user_id=session["user_id"],
                   book_id=books_result[0]["book_id"],
                   quote=quote)

        return redirect("/quotes")


@app.route("/book/<book_id>", methods=["GET", "POST", "DELETE"])
@login_required
def book(book_id):
    # loading book profile with data in it
    if request.method == "GET":
        data = db.execute("""SELECT * FROM books
                            WHERE book_id = :book_id
                             AND user_id = :user_id """,
                          book_id=book_id,
                          user_id=session["user_id"])
        print('BOOK PROFILE | data: ' + str(data), flush=True)

        quotes_result = db.execute("""SELECT * FROM quotes
                            JOIN books ON books.book_id = quotes.book_id
                            WHERE books.book_id = :book_id 
                            AND books.user_id = :user_id """,
                                   book_id=book_id,
                                   user_id=session["user_id"])
        print('BOOK PROFILE | quotes: ' + str(quotes_result), flush=True)

        lendings_result = db.execute("""SELECT * FROM lending
                            JOIN books ON books.book_id = lending.book_id
                            WHERE books.book_id = :book_id 
                            AND books.user_id = :user_id """,
                                     book_id=book_id,
                                     user_id=session["user_id"])
        print('BOOK PROFILE | lendings: ' + str(lendings_result), flush=True)

        return render_template("book.html", data=data, quotes=quotes_result, lendings=lendings_result)
    elif request.method == "POST":
        author = request.form.get("edit_author").title()  # capitalize first leter of every word
        print('EDIT BOOK | author: ' + str(author), flush=True)
        title = request.form.get("edit_title").capitalize()  # capitalize first letter
        print('EDIT BOOK | title: ' + str(title), flush=True)
        isbn = request.form.get("isbn")
        print('EDIT BOOK | isbn: ' + str(isbn), flush=True)
        page_count = request.form.get("edit_page_count")
        print('EDIT BOOK | page_count: ' + str(page_count), flush=True)
        genre = request.form.get("edit_genre")
        print('EDIT BOOK | genre: ' + str(genre), flush=True)
        belonging_check = request.form.get("edit_belonging_check")
        print('EDIT BOOK | belongingCheck: ' + str(belonging_check), flush=True)
        start_date = request.form.get("edit_start_date")
        start_date = None if not start_date else start_date
        print('EDIT BOOK | start_date: ' + str(start_date), flush=True)
        finish_date = request.form.get("edit_finish_date")
        finish_date = None if not finish_date else finish_date
        print('EDIT BOOK | finish_date: ' + str(finish_date), flush=True)
        ratings = request.form.get("edit_rating")
        print('EDIT BOOK | ratings: ' + str(ratings), flush=True)

        db.execute(
            """UPDATE books 
            SET title = :title, 
                author = :author, 
                pages = :pages, 
                isbn = :isbn, 
                genre = :genre, 
                rating = :rating, 
                started = :started, 
                finished = :finished, 
                owner = :owner
            WHERE book_id = :book_id""",
            title=title,
            author=author,
            pages=page_count,
            isbn=isbn,
            genre=genre,
            rating=ratings,
            started=start_date,
            finished=finish_date,
            owner=belonging_check,
            book_id=book_id)

        return redirect("/book/" + book_id)
    elif request.method == "DELETE":
        db.execute(""" DELETE FROM books WHERE book_id = :book_id""",
                   book_id=book_id)
        return 0


@app.route("/started-reading-book", methods=["POST"])
@login_required
def started_reading_book():
    if request.method == "POST":
        book_id = request.form.get("update_book_id")
        update_start_date = request.form.get("update_start_date")

        db.execute(
            """UPDATE books
            SET started = :update_start_date
            WHERE book_id = :book_id""",
            update_start_date=update_start_date,
            book_id=book_id)

        return redirect("/")


@app.route("/finished-reading-book", methods=["POST"])
@login_required
def finished_reading_book():
    if request.method == "POST":
        book_id = request.form.get("update_book_id")
        update_finish_date = request.form.get("update_finish_date")

        db.execute(
            """UPDATE books
            SET finished = :update_finish_date
            WHERE book_id = :book_id""",
            update_finish_date=update_finish_date,
            book_id=book_id)

        return redirect("/")


@app.route("/not-reading-book", methods=["POST"])
@login_required
def not_reading_book():
    if request.method == "POST":
        dict_str = request.data.decode("UTF-8")
        data = ast.literal_eval(dict_str)

        book_id = data['bookId']

        db.execute(
            """UPDATE books
            SET started = NULL
            WHERE book_id = :book_id""",
            book_id=book_id)

        return 0


@app.route("/delete-book", methods=["POST"])
@login_required
def delete_book():
    if request.method == "POST":
        dict_str = request.data.decode("UTF-8")
        data = ast.literal_eval(dict_str)

        book_id = data['bookId']

        db.execute(""" DELETE FROM books WHERE book_id = :book_id""",
                   book_id=book_id)

        return 0


@app.route("/book/<book_id>/update-notes", methods=["POST"])
@login_required
def update_notes(book_id):
    notes = request.form.get("note_text")

    db.execute("""UPDATE books 
               SET notes = :notes 
               WHERE book_id = :book_id""",
               notes=notes,
               book_id=book_id)

    return redirect("/book/" + book_id)


@app.route("/book/<book_id>/new-quote", methods=["POST"])
@login_required
def book_new_quote(book_id):
    quote = request.form.get("quote")

    db.execute("INSERT INTO quotes (user_id, book_id, quote) VALUES (:user_id, :book_id, :quote)",
               user_id=session["user_id"],
               book_id=book_id,
               quote=quote)

    return redirect("/book/" + book_id)


@app.route("/book/<book_id>/update-quote/<quote_id>", methods=["POST"])
@login_required
def update_quote(book_id, quote_id):
    quote_text = request.form.get("quote_text")

    db.execute("""UPDATE quotes 
               SET quote = :quote_text 
               WHERE quote_id = :quote_id""",
               quote_text=quote_text,
               quote_id=quote_id)

    return redirect("/book/" + book_id)


@app.route("/book/<book_id>/delete-quote/<quote_id>", methods=["POST"])
@login_required
def delete_quote(book_id, quote_id):
    db.execute("""DELETE FROM quotes WHERE quote_id = :quote_id""",
               quote_id=quote_id)

    return redirect("/book/" + book_id)


@app.route("/book/<book_id>/lending", methods=["POST"])
@login_required
def add_book_lending(book_id):
    lent_to = request.form.get("lent_to")
    lent_date = request.form.get("lent_date")
    lent_date = None if not lent_date else lent_date
    returned_date = request.form.get("returned_date")
    returned_date = None if not returned_date else returned_date

    db.execute("""INSERT INTO lending 
                  (user_id, book_id, borrower, lent_date, returned) 
                  VALUES 
                  (:user_id, :book_id, :borrower, :lent_date, :returned)""",
               user_id=session["user_id"],
               book_id=book_id,
               borrower=lent_to,
               lent_date=lent_date,
               returned=returned_date)

    update_book_if_lent(book_id)

    return redirect("/book/" + book_id)


@app.route("/book/<book_id>/lending/<lend_id>", methods=["POST"])
@login_required
def edit_book_lending(book_id, lend_id):
    lent_to = request.form.get("lent_to")
    lent_date = request.form.get("lent_date")
    lent_date = None if not lent_date else lent_date
    returned_date = request.form.get("returned_date")
    returned_date = None if not returned_date else returned_date

    db.execute("""UPDATE lending 
                  SET borrower = :borrower,
                      lent_date = :lent_date,
                      returned = :returned
                  WHERE lend_id = :lend_id""",
               borrower=lent_to,
               lent_date=lent_date,
               returned=returned_date,
               lend_id=lend_id)

    update_book_if_lent(book_id)

    return redirect("/book/" + book_id)


def update_book_if_lent(book_id):
    lent_data = db.execute("""SELECT * FROM lending
                                WHERE book_id = :book_id 
                                AND returned IS NULL""",
                           book_id=book_id)

    db.execute("""UPDATE books
                   SET lent = :lent
                   WHERE book_id = :book_id""",
               lent=len(lent_data) != 0,
               book_id=book_id)


@app.route("/book/<book_id>/delete-lending/<lend_id>", methods=["POST"])
@login_required
def delete_book_lending(book_id, lend_id):
    db.execute("""DELETE FROM lending WHERE lend_id = :lend_id""",
               lend_id=lend_id)

    return redirect("/book/" + book_id)


@app.route("/all", methods=["GET", "POST"])
@login_required
def all_books():
    if request.method == "POST":
        return redirect("/quotes")
