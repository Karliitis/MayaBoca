function deleteTask(taskId) {
    fetch("/delete-task", {
        method: "POST",
        body: JSON.stringify({taskId: taskId})
    }).then((_) => {
        window.location.href = "/tasks"
    })
}

function deleteQuestion(questionId) {
    const parameters = window.location.search;
    fetch("/delete-question", {
        method: "POST",
        body: JSON.stringify({questionId: questionId})
    }).then((_) => {
        window.location.href = "/tasks/questions" + parameters
    })
}