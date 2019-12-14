const baseUrl = 'http://127.0.0.1:8000/api_v1/';
console.log('HIIIIII')
function getFullPath(path) {
    path = path.replace(/^\/+|\/+$/g, '');
    path = path.replace(/\/{2,}/g, '/');
    return baseUrl + path + '/';
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// var csrftoken = getCookie('csrftoken');

function makeRequest(path, method, auth=true, data=null) {
    let settings = {
        url: getFullPath(path),
        method: method,
        dataType: 'json'
    };
    if (data) {
        settings['data'] = JSON.stringify(data);
        settings['contentType'] = 'application/json';
    }
    if (auth) {
        settings.headers = {'X-CSRFToken': getCookie('csrftoken')};
    }

    return $.ajax(settings);
}

let quoteForm, homeLink, formSubmit, formTitle, buttons, formModal,
    authorInput, textInput,createLink, updateLink, ratingUpdate,
    textUpdate, updateForm, quoteEditForm, fotocommentInput;

function setUpGlobalVars() {
    quoteForm = $('#quote_form');
    updateForm = $('#update_form');
    updateLink = $('#edit_');
    homeLink = $('#home_link');
    updateLink = $('#update_link');
    createLink = $('#create_link');
    formSubmit = $('#form_submit');
    formTitle = $('#form_title');
    buttons = $('#buttons');
    formModal = $('#form_modal');
    authorInput = $('#author');
    textInput = $('#text');
    textUpdate = $('#text_update');
    ratingUpdate = $('#rating_update');
    quoteEditForm = $('#quote_edit_form')
    fotocommentInput = $('#fotocomment')

}


function rateUp(id) {
    let request = null;
    let token = getCookie('csrftoken');
    if (token) {
        request = makeRequest('foto/' + id + '/rate_up', 'post', true);
    }else {
        request = makeRequest('foto/' + id + '/rate_up', 'post', false);
    }
    request.done(function(data, status, response) {
        console.log('Rated up quote with id ' + id + '.');
        $('#rating_' + id).text(data.rating);
    }).fail(function(response, status, message) {
        console.log('Could not rate up quote with id ' + id + '.');
        console.log(getCookie('csrftoken'));
        console.log(response.responseText);
    });
}

function rateDown(id) {
    let request = null;
    let token = getCookie('csrftoken');
    if (token) {request = makeRequest('foto/' + id + '/rate_down', 'post', true);}
    else{request = makeRequest('foto/' + id + '/rate_down', 'post', false);}
    request.done(function(data, status, response) {
        console.log('Rated down quote with id ' + id + '.');
        $('#rating_' + id).text(data.rating);
    }).fail(function(response, status, message) {
        console.log('Could not rate down quote with id ' + id + '.');
        console.log(response.responseText);
    });
}

function deleteComment(id){
    let request =  makeRequest('comments/' + id, 'delete', true);
    request.done(function(item)
    {
        getComment();
    }
    ).fail(function(response, status, message){
        console.log('Коммент не удаляется!');
        console.log(response.responseText);
    });

}

function updateComment(){
    quoteForm.on('submit', function(event) {
        event.preventDefault();
        console.log('yes');
        addQuote(textInput.val(), authorInput.val(), fotocommentInput.val());
    });

    updateLink.on('click', function(event) {
        event.preventDefault();
        // logInForm.addClass('d-none');
        quoteForm.removeClass('d-none');
        formTitle.text('Обновить');
        formSubmit.text('Сохранить');
        formSubmit.off('click');
        formSubmit.on('click', function(event) {
            quoteForm.submit()
        });
    });
}

function getClicks(id){
    console.log(id);
    let request =  makeRequest('foto/' + id, 'get', true);
    request.done(function(item)
    {
        console.log(item, 'SPARTA');
        buttons.empty();
        buttons.append($(`
                <p id="rating_${item.id}">Количество лайков: ${item.rating}</p>
                <a href="#" class="btn btn-danger" id="rate_down_${item.id}">-</a>
                <a href="#" class="btn btn-success" id="rate_up_${item.id}">+</a>
                </p>`));
        $('#rate_up_' + item.id).on('click', function(event) {
                console.log('click');
                event.preventDefault();
                rateUp(item.id);
            });
            $('#rate_down_' + item.id).on('click', function(event) {
                console.log('click');
                event.preventDefault();
                rateDown(item.id);
            });
    }
    ).fail(function(response, status, message){
        console.log('Кнопки не работают!');
        console.log(response.responseText);
    });

}

function getComment(item){
    quoteForm.on('submit', function(event) {
        event.preventDefault();
        console.log('yes');
        addQuote(textInput.val(), authorInput.val(), fotocommentInput.val());
    });

    createLink.on('click', function(event) {
        event.preventDefault();
        // logInForm.addClass('d-none');
        quoteForm.removeClass('d-none');
        formTitle.text('Создать');
        formSubmit.text('Сохранить');
        formSubmit.off('click');
        formSubmit.on('click', function(event) {
            quoteForm.submit()
        });
    });
}

function addQuote(fotocomment, text, author) {
    let request = null;
    let token = getCookie('csrftoken');
    const credentials = {fotocomment, text, author};
    if (token) {request = makeRequest('comments', 'post', true, credentials);}
    else{request = makeRequest('comments', 'post', false, credentials);}

    request.done(function (data) {
        formModal.modal('hide');
        }
    ).fail(function (response, status, message) {
        console.log('Комментарий не создан!');
        console.log(response.responseText);
    });
}

$(document).ready(function() {
    setUpGlobalVars();
    // setUpAuth();
    // checkAuth();
    // getClicks();
    getComment();

});