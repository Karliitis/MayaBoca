function deleteTask(taskId) {
    fetch("/delete-task", {
        method: "POST",
        body: JSON.stringify({taskId: taskId})
    }).then((_) => {
        window.location.href = "/tasks"
    })
}

function deleteQuestion(questionId) {
    const search = window.location.search;
    fetch("/delete-question", {
        method: "POST",
        body: JSON.stringify({questionId: questionId})
    }).then((_) => {
        window.location.href = "/tasks/questions" + search
    })
}

function deleteAnswer(answerId) {
    const search = window.location.search;
    fetch(window.location.origin + "/delete-answer", {
        method: "POST",
        body: JSON.stringify({answerId: answerId}),
        headers: {"Accept": "application/json"}
    }).then((_) => {
        var answer_box = document.getElementById("div" + answerId)
        answer_box.remove()
        // window.location.href = "/tasks/questions/question" + search
    })
}

function addAnswer() {
    const search = window.location.search
    const parameters = new URLSearchParams(search)
    fetch(window.location.origin + "/add-answer", {
        method: "POST",
        body: JSON.stringify({questionId: parameters.get("question")}),
        headers: {"Accept": "application/json"}
    }).then(response => response.json()).then(response => {
        // response = JSON.stringify(response)
        var elem = document.querySelector(".answer")
        var elem_copy = elem.cloneNode(true)
        elem_copy.id = "box" + response["answerId"]

        var input = elem_copy.getElementsByTagName("input").item(0)
        input.id = "input" + response["answerId"]
        input.name = response["answerId"]
        input.value = ""

        var delete_btn = elem_copy.getElementsByTagName("button").item(0)
        delete_btn.setAttribute("onclick", "deleteAnswer('" + response["answerId"] + "')")
        console.log(delete_btn)
        
        console.log(elem_copy)
        document.getElementById("answers").appendChild(elem_copy)
    })
}