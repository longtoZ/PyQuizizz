document.querySelector('.send').addEventListener('click', function() {
    let input_value = document.querySelector('.search-bar').value.trim()
    let error = document.querySelector('.error')

    if (!input_value.includes('https://quizizz.com/')) {
        error.style.display = 'inline-block'
        error.textContent = 'Not a Quizizz link!'
    } else {
        error.style.display = ''
        error.textContent = ''
        document.querySelector('.submit').click()
        document.querySelector('.loader').style.display = 'block'
    }
})

document.querySelector('.clear').addEventListener('click', function() {
    document.querySelector('.search input').value = ''
})

if (document.querySelector('.show-options')) {

    document.querySelectorAll('tr').forEach(j => {
        const td = j.querySelectorAll('td')
        if (td.length > 0) {
            const ques = td[0]
            const ans = td[1]

            ques.innerHTML = `<div>${ques.textContent.replace('&lt;', '<').replace('&gt;', '>')}</div>`
            ans.innerHTML = `<div>${ans.textContent}</div>`
        }
    })

    let show = false
    const options = document.querySelectorAll('.options')
    const show_btn = document.querySelector('.show-options')
    // Function to switch options button
    if (show_btn) {
        show_btn.addEventListener('click', function() {
            if (show == false) {
                show = true
                show_btn.textContent = 'Hide options'
                show_btn.classList.remove('options-hide')
                show_btn.classList.add('options-show')
        
                options.forEach(i => {
                    i.style.display = "block"
                })
            } else {
                show = false
                show_btn.textContent = 'Show options'
                show_btn.classList.remove('options-show')
                show_btn.classList.add('options-hide')
        
                options.forEach(i => {
                    i.style.display = "none"
                })
            }
        })
    }

    // Function to convert HTML table to CSV format
    function convertTableToCSV(data) {
        let csvData = 'No.,Question,Options,Answer\n'
        for (i of data) {
            row = []
            for (j of i) {
                if (Array.isArray(j)) {
                    row.push(`"${j.map(k => k.replaceAll('"','""')).join('\n')}"`)
                } else {
                    row.push(`"${j.replaceAll('"','""')}"`)
                }
            }

            csvData += row.join(',') + '\n'
        }

        // console.log(csvData)
        return csvData
    }

    // Function to download the CSV file
    function downloadCSV(csvData) {
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${document.querySelector('.result-title').textContent.replace(' ', '_')}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    // Attach click event to the download button
    document.querySelector('.save-type').addEventListener('click', () => {
        const csvData = convertTableToCSV(data);
        downloadCSV(csvData);
    });

    function findWord() {
        let input = document.querySelector('.find').value.trim()

        document.querySelectorAll('tr').forEach(i => {
            if (i.querySelector('th') == null) {
                let text = i.textContent.replaceAll('\t', '').trim()
                if (!text.match(new RegExp(input, "i"))) {
                    i.style.display = 'none'
                } else {
                    i.style.display = ''
                }
            }
        })
    }

    String.prototype.replaceAt = function(index, replacement) {
        return this.substring(0, index) + replacement + this.substring(index + 1);
    }
}
