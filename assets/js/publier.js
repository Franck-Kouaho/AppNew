// var editor = new Editor({
// element: document.getElementById('comment-text-area'),
// toolbar: false,
// status: false
// })
// editor.render();

var previewPicture = function(e){
    const[picture] = e.files
    var image_url = ''
    debugger
    if(picture){
        image_url = URL.createObjectURL(picture)
        image.src = image_url;
    }
}

sendReq = function(req_url, form = null, queryMethod='POST'){
    var HttpRequest = new XMLHttpRequest();
    var token_input = document.querySelector('input[name="csrfmiddlewaretoken"]')     
    HttpRequest.open(queryMethod, req_url, true);
    HttpRequest.setRequestHeader("X-CSRFToken", token_input.value)
    if(form != null){
        var data = new FormData(form);
        HttpRequest.send(data);
    }else{
        HttpRequest.send(data);
    }
    return HttpRequest
}
send_btn = document.querySelector('.send_btn')
formulaire = document.querySelector('#publication_form')
formulaire.addEventListener('submit', function(e){
    e.preventDefault()
    //formulaire.querySelector('#comment').value = editor.codemirror.getValue()
    debugger
    req = sendReq(this.action, this)
    req.onreadystatechange = function() {
        if (req.readyState === 4) {
            debugger
            response = JSON.parse(req.response)
            if(req.status === 200 && response.is_connect === false){
                window.location.replace(window.location.href.replace("#",""))
            }else(
                alert(response.message)
            )
        }
    }
})

/*
                SOUS-CATEGORIES
*/

var select_category = document.querySelector('#categoryID')
var select_subcategeory = document.querySelector('#subcategoryID')
loadSubCategory = function(){
    var subcategory_link = '/get-sub-category/'+select_category.value+'/'
    req = sendReq(subcategory_link, null, queryMethod='GET')
    req.onreadystatechange = function() {
        if (req.readyState === 4) {
            if(req.status === 200){
                response = JSON.parse(req.response)
                select_subcategeory.innerHTML=''
                for (key in response){
                    catOption = document.createElement('option')
                    catOption.value=key
                    catOption.innerText=response[key]
                    select_subcategeory.appendChild(catOption)
                }
            }else(
                alert(response.message)
            )
        }
    }
}
select_category.addEventListener('change', function(e){
    loadSubCategory()
})

loadSubCategory()