var app = new Vue({
  el: '#app',
  data: {
    messages: [],
    active: {}  // {message, plain, html}
  },
  methods: {
      refresh: function () {
        this.$http.get('/messages').then(
          function (response) {
            this.messages = response.data
          }
        )
      },
      activate: function (msg) {
        this.active = {message: msg, state: 'headers'}
      },
      add: function (msg) {
        this.messages.splice(0, 0, msg)
      },
      remove: function (msg_id) {
        var idx = this.messages.findIndex(function (msg) {return msg.id == msg_id})
        if (idx >= 0) {
          this.messages.splice(idx, 1)
        }

        if (this.active.message !== undefined & this.active.message.id === msg_id) {
          this.active = {}
        }
      },
      showHeaders: function(msg) {
        this.active.state = 'headers'
      },
      showPlain: function(msg) {
        this.active.state = 'plain'
        if (this.active.plain === undefined) {
          this.$http.get('/messages/' + msg.id + '/plain').then(
            function (response) {
              this.active.plain = response.data
              this.$forceUpdate()
            }
          )
        }
      },
      showHtml: function(msg) {
        this.active.state = 'html'
        if (this.active.html === undefined) {
          this.$http.get('/messages/' + msg.id + '/html').then(
            function (response) {
              this.active.html = response.data
              this.$forceUpdate()
            }
          )
        }
      },
      showRaw: function(msg) {
        this.active.state = 'raw'
        if (this.active.raw === undefined) {
          this.$http.get('/messages/' + msg.id + '/raw').then(
            function (response) {
              this.active.raw = response.data
              this.$forceUpdate()
            }
          )
        }
      },
      download: function(msg) {
        console.log('download()')
      }
  }
})

app.refresh()

var _arr = window.location.href.split("/");
var hostport = _arr[2]
_arr = undefined

var ws = new WebSocket('ws://' + hostport + '/ws');
ws.onmessage = function (event) {
  var data = JSON.parse(event.data)
  if (data.action == 'received') {
    app.add(data.message)
  } else if (data.action == 'removed') {
    app.remove(data.message.id)
  }
}
