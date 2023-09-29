document.addEventListener('DOMContentLoaded', function () {
    const table = document.querySelector('table');
    const thElements = document.querySelectorAll('th');
    const resetButton = document.getElementById('resetButton');
    const courseData = document.getElementById('course-data');
    const lastUpdate = document.getElementById('lastUpdate');
    const loadDataButton = document.getElementById('loadDataButton');
    const courseAbbreviationSelect = document.getElementById('courseAbbreviation');

    function loadCourseData(abbreviation) {
        courseData.innerHTML = '';

        fetch(`/get_course_data/${abbreviation}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(course => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${course.CRN}</td>
                        <td>${course['Course Code']}</td>
                        <td>${course['Course Title']}</td>
                        <td>${course['Teaching Method']}</td>
                        <td>${course.Instructor}</td>
                        <td>${course.Building}</td>
                        <td>${course.Day}</td>
                        <td>${course.Time}</td>
                        <td>${course.Room}</td>
                        <td>${course.Capacity}</td>
                        <td>${course.Enrolled}</td>
                        <td>${course.Reservation}</td>
                        <td>${course['Major Restriction']}</td>
                        <td>${course.Prerequisites}</td>
                        <td>${course['Class Restrictions']}</td>
                        <td>${course['No Capacity']}</td>
                    `;
                    courseData.appendChild(row);
                });

                if (data.length > 0) {
                    const lastUpdateData = data[data.length - 1];
                    if (lastUpdateData && lastUpdateData['Last Update']) {
                        lastUpdate.textContent = `Last Update: ${lastUpdateData['Last Update']}`;
                        removeLastRow();
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    resetButton.addEventListener('click', () => {
        thElements.forEach(th => {
            th.style.display = 'table-cell';
        });

        const tdElements = document.querySelectorAll('td');
        tdElements.forEach(td => {
            td.style.display = 'table-cell';
        });
    });

    loadDataButton.addEventListener('click', () => {
        const selectedAbbreviation = courseAbbreviationSelect.value;
        loadCourseData(selectedAbbreviation);
    });

    function removeLastRow() {
        const rows = table.getElementsByTagName('tr');
        if (rows.length > 0) {
            table.deleteRow(rows.length - 1);
        }
    }

    thElements.forEach(th => {
        th.addEventListener('click', () => {
            toggleColumn(th.dataset.column);
        });
    });

    function toggleColumn(columnName) {
        const columnIndex = Array.from(thElements).findIndex(th => th.dataset.column === columnName);
        const tdElements = document.querySelectorAll(`td:nth-child(${columnIndex + 1})`);

        if (thElements[columnIndex].style.display === '' || thElements[columnIndex].style.display === 'table-cell') {
            thElements[columnIndex].style.display = 'none';
            tdElements.forEach(td => td.style.display = 'none');
        } else {
            thElements[columnIndex].style.display = 'table-cell';
            tdElements.forEach(td => td.style.display = 'table-cell');
        }
    }
});
