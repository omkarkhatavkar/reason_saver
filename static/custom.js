$.datetimepicker.setDateFormatter({
    parseDate: function (date, format) {
        var d = moment(date, format);
        return d.isValid() ? d.toDate() : false;
    },
    formatDate: function (date, format) {
        return moment(date).format(format);
    },
});

$('.datetime').datetimepicker({
    format:'DD-MM-YYYY hh:mm A',
    formatTime:'hh:mm A',
    formatDate:'DD-MM-YYYY',
    useCurrent: false,
});

// Initialise Pusher
const pusher = new Pusher('f9f11e109c74b46611d2', {
    cluster: 'ap2',
    encrypted: true
});

var channel = pusher.subscribe('my-channel');

channel.bind('my-event', (data) => {

   $('#failures').append(`
        <tr id="${data.data.id}">
            <th scope="row"> ${data.data.failure} </th>
            <td> ${data.data.count} </td>
            <td> ${data.data.status} </td>
        </tr>
   `)
});

channel.bind('update-record', (data) => {

    $(`#${data.data.id}`).html(`
        <th scope="row"> ${data.data.failure} </th>
        <td> ${data.data.count} </td>
        <td> ${data.data.status} </td>
    `)

 });