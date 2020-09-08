// Inserts current date in the appropiate format for the "reading now" date input but just once
$("#btnTwo").one("click", function () {
    let date = new Date();

    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    let today = year + "-" + month + "-" + day;
    $("#dateReadingNow").attr("value", today);
});


// Selecting bootstrap accordion card is reseting values of another accordion card - for the sake of writting values of just one card (if both of the cards have some input in)
function ClearFieldsOne() {
    document.getElementById("start_date").value = "";
    document.getElementById("finish_date").value = "";
}

function ClearFieldsTwo() {
    document.getElementById("dateReadingNow").value = "";
}

//Get the value of a star rating to be able to insert it into database
$('#5stars').click(function () {
    $('#ratings').val('5');
    removeMarkedStars();
    $('#5stars').addClass('marked');
    $('#4stars').addClass('marked');
    $('#3stars').addClass('marked');
    $('#2stars').addClass('marked');
    $('#1stars').addClass('marked');
});

$('#4stars').click(function () {
    $('#ratings').val('4');
    removeMarkedStars();
    $('#4stars').addClass('marked');
    $('#3stars').addClass('marked');
    $('#2stars').addClass('marked');
    $('#1stars').addClass('marked');
});

$('#3stars').click(function () {
    $('#ratings').val('3');
    removeMarkedStars();
    $('#3stars').addClass('marked');
    $('#2stars').addClass('marked');
    $('#1stars').addClass('marked');
});

$('#2stars').click(function () {
    $('#ratings').val('2');
    removeMarkedStars();
    $('#2stars').addClass('marked');
    $('#1stars').addClass('marked');
});

$('#1stars').click(function () {
    $('#ratings').val('1');
    removeMarkedStars();
    $('#1stars').addClass('marked');
});

function removeMarkedStars() {
    $('#5stars').removeClass('marked');
    $('#4stars').removeClass('marked');
    $('#3stars').removeClass('marked');
    $('#2stars').removeClass('marked');
    $('#1stars').removeClass('marked');
}


// ISBN validation
$(document).ready(function () {
    function validate(e) {

        let Reg = /^$|^(?:\d[ |-]?){13}$/;
        let isbn = document.getElementById('isbn');

        if (Reg.test(isbn.value) === false) {
            var invalid_isbn = document.createTextNode("Invalid ISBN");
            var error_message = document.getElementById("error_message");
            if (!error_message.firstChild) {
                error_message.appendChild(invalid_isbn);
            }
            isbn.focus();
            e.preventDefault(); // prevent the form sending
        } else {
            let error_message = document.getElementById("error_message");
            if (error_message.firstChild) {
                error_message.removeChild(error_message.firstChild)
            }
        }
    }

    //add event listener for form submission
    document.getElementById('edit-book-form').addEventListener('submit', validate);
});


// Redirects to book page when this function is called.
// Should not proceed with redirection if action originates from options menu.
function redirectToBook(bookId) {
    let shouldRedirect = true;
    event.composedPath().forEach(domElement => {
        if (domElement.classList && domElement.classList.contains('options'))
            shouldRedirect = false;
    })

    if (shouldRedirect) {
        localStorage.clear();
        document.location.href = '/book/' + bookId;
    }
}

// ---------------------- GLOBAL OPTIONS START --------------------------------

let openedOptions = null;

// Function to show options when triple dot is clicked.
// Hides when same dots are pressed.
// Hides first dropdown menu if second is pressed while first one is still showed.
function showOptionsFor(optionsId) {
    const clickedOptions = document.getElementById(optionsId);
    if (openedOptions) {
        openedOptions.classList.remove('show');
    }

    if (openedOptions !== clickedOptions) {
        openedOptions = clickedOptions;
        openedOptions.classList.toggle("show");
    } else {
        openedOptions = null;
    }
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.options_image')) {
        let options_content = document.getElementsByClassName("options_content");
        let i;
        for (i = 0; i < options_content.length; i++) {
            let openDropdown = options_content[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
        if (!event.target.matches('.book_options_image')) {
            let options_content = document.getElementsByClassName("book_options_content");
            let i;
            for (i = 0; i < options_content.length; i++) {
                let openDropdown = options_content[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
            if (!event.target.matches('.note_options_image')) {
                let options_content = document.getElementsByClassName("note_options_content");
                let i;
                for (i = 0; i < options_content.length; i++) {
                    let openDropdown = options_content[i];
                    if (openDropdown.classList.contains('show')) {
                        openDropdown.classList.remove('show');
                    }
                }
                if (!event.target.matches('.book_quote_options_image')) {
                    let options_content = document.getElementsByClassName("book_quote_options_content");
                    let i;
                    for (i = 0; i < options_content.length; i++) {
                        let openDropdown = options_content[i];
                        if (openDropdown.classList.contains('show')) {
                            openDropdown.classList.remove('show');
                        }
                    }
                    if (!event.target.matches('.book_lend_options_image')) {
                        let options_content = document.getElementsByClassName("book_lend_options_content");
                        let i;
                        for (i = 0; i < options_content.length; i++) {
                            let openDropdown = options_content[i];
                            if (openDropdown.classList.contains('show')) {
                                openDropdown.classList.remove('show');
                            }
                        }
                        openedOptions = null;
                    }
                }
            }
        }
    }
}

// ---------------------- GLOBAL OPTIONS END --------------------------------
// ---------------------- BOOK OPTIONS START --------------------------------

// Update #readingNowModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#readingNowModal').on('show.bs.modal', updateModalWithBookId)

// Update #finishedReadingModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#finishedReadingModal').on('show.bs.modal', updateModalWithBookId)

// Update #deleteBookConfirmationModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#deleteBookConfirmationModal').on('show.bs.modal', updateModalWithBookId)

function updateModalWithBookId(event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')

    let modal = $(this)
    modal.find('.modal-content #update_book_id').val(bookId)
}


// Sends DELETE request to delete book with bookId from the database.
// When response is retrieved - refreshes index page.
$('#confirmBookDeleteFromList').click(function () {
    let modal = $(this)  //Delete confirmation button
    let bookId = modal.find('+ #update_book_id').val(); //Find #update_book_id input which is next to delete confirmation button

    let book = {"bookId": bookId};
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/delete-book", true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        location.reload();
    };
    xhr.send(JSON.stringify(book));
})

// Sends DELETE request to delete book with bookId from the database.
// When response is retrieved - refreshes index page.
$('#confirmBookDelete').click(function () {
    let modal = $(this)  //Delete confirmation button
    let bookId = modal.find('+ #update_book_id').val(); //Find #update_book_id input which is next to delete confirmation button

    let xhr = new XMLHttpRequest();
    xhr.open("DELETE", "/book/" + bookId, true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        location.href = "/";
    };
    xhr.send();
})


// Sends POST request to mark book with bookId as currently not being read by the user.
function notReading(bookId) {
    let book = {"bookId": bookId};
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/not-reading-book", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        location.reload();
    };
    xhr.send(JSON.stringify(book));
}

// Update #editBookModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#editBookModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget);
    let bookId = actionOrigin.data('bookid');
    let bookData = actionOrigin.data('bookdata');
    let correctedBookData = bookData.replace(/'/g, '"').replace(/None/g, 'null');
    let book = JSON.parse(correctedBookData);

    let modal = $(this);
    modal.find('.modal-content #edit_author').val(book.author);
    modal.find('.modal-content #edit_title').val(book.title);
    modal.find('.modal-content #isbn').val(book.isbn);
    modal.find('.modal-content #edit_page_count').val(book.pages);
    modal.find('.modal-content #edit_genre').val(book.genre);
    modal.find('.modal-content #edit_belonging_check').prop('checked', book.owner !== null);
    modal.find('.modal-content #edit_rating').val(book.rating);
    modal.find('.modal-content #edit_start_date').val(book.started);
    modal.find('.modal-content #update_finish_date').val(book.finished);

    document.getElementById('edit-book-form').action = "/book/" + bookId;
})

// ---------------------- BOOK OPTIONS END --------------------------------
// ---------------------- NOTE OPTIONS START --------------------------------

// Update #editNoteModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#editNoteModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')
    let noteText = actionOrigin.data('notetext')

    let modal = $(this)
    modal.find('.modal-content #note_text').val(noteText)
    document.getElementById('edit-note-form').action = "/book/" + bookId + "/update-notes";
})

// Update #deleteNoteConfirmationModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#deleteNoteConfirmationModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')

    document.getElementById('delete-note-form').action = "/book/" + bookId + "/update-notes";
})

// ---------------------- NOTE OPTIONS END --------------------------------
// ---------------------- QUOTE OPTIONS START --------------------------------

// Update #editBookQuoteModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#editBookQuoteModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')
    let quoteId = actionOrigin.data('quoteid')
    let quoteText = actionOrigin.data('quotetext')

    let modal = $(this)
    modal.find('.modal-content #quote_text').val(quoteText)
    document.getElementById('edit-quote-form').action = "/book/" + bookId + "/update-quote/" + quoteId;
})

// Update #deleteBookQuoteConfirmationModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#deleteBookQuoteConfirmationModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')
    let quoteId = actionOrigin.data('quoteid')

    document.getElementById('delete-quote-form').action = "/book/" + bookId + "/delete-quote/" + quoteId;
})

// ---------------------- QUOTE OPTIONS END --------------------------------
// ---------------------- LENDING OPTIONS START --------------------------------
// Update #addBookLendingModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#bookLendingModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')
    let lendId = actionOrigin.data('lendid')

    if (lendId) {
        let modal = $(this)
        modal.find('.modal-title').text("Edit lending")

        let lendId = actionOrigin.data('lendid')
        let lendData = actionOrigin.data('lenddata');
        let correctedLendData = lendData.replace(/'/g, '"').replace(/None/g, 'null');
        let lend = JSON.parse(correctedLendData);

        modal.find('.modal-content #lent_to').val(lend.borrower);
        modal.find('.modal-content #lent_date').val(lend.lent_date);
        modal.find('.modal-content #returned_date').val(lend.returned);

        document.getElementById('lending-form').action = "/book/" + bookId + "/lending/" + lendId;
    } else {
        let modal = $(this)
        modal.find('.modal-title').text("Lend a book")

        modal.find('.modal-content #lent_to').val(null);
        modal.find('.modal-content #lent_date').val(null);
        modal.find('.modal-content #returned_date').val(null);

        document.getElementById('lending-form').action = "/book/" + bookId + "/lending";
    }
})

// Update #deleteBookQuoteConfirmationModal contents before it is shown.
// 'show.bs.modal' is a default bootstrap event which triggers when modal is about to be shown.
$('#deleteBookLendingConfirmationModal').on('show.bs.modal', function (event) {
    openedOptions = null;

    let actionOrigin = $(event.relatedTarget)
    let bookId = actionOrigin.data('bookid')
    let lendId = actionOrigin.data('lendid')

    document.getElementById('delete-lending-form').action = "/book/" + bookId + "/delete-lending/" + lendId;
})

// ---------------------- LENDING OPTIONS END --------------------------------

// ------------------------CHECKBOX-----------------------------------------
// change checkform value when it is clicked
function checkValue() {
    var inputList = document.getElementById('inputList');
    localStorage.setItem('selectVal', inputList.value);

    var checkbox = document.getElementById('defaultCheck1');

    if (localStorage.selectVal === 'lent') {
        document.getElementById("defaultCheck1").setAttribute("disabled", true)
    } else {
        document.getElementById("defaultCheck1").removeAttribute("disabled");
    }

    localStorage.setItem('checkboxValue', checkbox.checked);
    if (checkbox.checked === true) {
        document.getElementById("defaultCheck1").setAttribute("value", "True")
    } else if (checkbox.checked !== true) {
        document.getElementById("defaultCheck1").setAttribute("value", "False")
    }
    $('#listform').submit();
}

$(document).ready(function () {
    if (localStorage.selectVal) {
        $('#inputList').val(localStorage.selectVal);
    }
    $(this).find('#defaultCheck1').prop('checked', localStorage.checkboxValue === 'true');

    if (localStorage.selectVal === 'lent') {
        document.getElementById("defaultCheck1").setAttribute("disabled", true)
    } else {
        document.getElementById("defaultCheck1").removeAttribute("disabled");
    }
});

$('#inputList').on('change', checkValue);