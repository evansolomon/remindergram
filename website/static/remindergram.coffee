$ ->
	# Dom elements
	$form       = $ 'form.remindergram'
	$identifier = $ '#identifier'
	$result     = $ '.result'

	# Service/identify map
	services =
		'Instagram' : 'Username'
		'WordPress' : 'Blog address'
		'Tumblr'    : 'Blog address'
		'RSS'       : 'Feed address'

	# AJAX requests
	activeRequest = false
	lastQuery     = {}
	requestCache  = {}

	# Listen on service buttons
	$form.find( '.btn' ).on 'click', ( event ) ->
		event.preventDefault()
		$form.find( '.btn' ).removeClass 'active'
		$( this ).addClass 'active'
		doService $( event.target ).text()
		$identifier.focus()

	getActiveService = ->
		active = $form.find '.btn.active'
		if active
			active.text()
		else
			''

	doService = ( name )->
		setIdentifer services[name]

	setIdentifer = ( placeholder ) ->
		$( 'label[for="identifier"]' ).text "Enter #{placeholder}"
		$identifier.attr 'placeholder', placeholder

	# Listen on form submit
	$form.on 'submit', ( event ) ->
		event.preventDefault()

		data = parseFormData $form
		return if _.contains _.values( data ), ''

		return if _.isEqual data, @lastQuery

		@lastQuery = data

		hash = hashRequest data
		if _.has requestCache, hash
			return renderResponse requestCache[hash]

		@activeRequest.abort() if @activeRequest
		@activeRequest = sendRequest data

	hashRequest = ( data ) ->
		_.pairs( data ).toString()

	sendRequest = ( data ) ->
		waitingPanda()
		$.post $form.attr( 'action' ), data, ( response ) ->
			cacheResponse data, response
			renderResponse response

	renderResponse = ( response ) ->
		if response.error
			renderError response
		else
			renderSucces response

	cacheResponse = ( data, response ) ->
		hash = hashRequest data
		requestCache[hash] = response

	# Auto-submit form when the user stops typing
	$form.keyup _.debounce ->
		$form.submit()
	, 800

	parseFormData = ( $form ) ->
		inputs = _.reduce $form.serializeArray(), ( data, pair ) ->
			data[ pair.name ] = pair.value
			return data
		, {}

		_.extend inputs, { 'service': getActiveService() }

	renderSucces = ( response ) ->
		compiled = _.template '
			<ul>
			<% _.each(photos, function(photo) { %>
				<li><div class="crop"><img src="<%= photo %>"></div></li> <%
			}); %>
			</ul>',
			photos: response

		renderResult compiled

	renderError = ( response ) ->
		compiled = _.template 'Oops, there was an error: <%= error %>', response
		renderResult compiled

	renderResult = ( html ) ->
		$result.html html

	waitingPanda = ->
		compiled = _.template '<p class="waiting"><img src="<%= src %>" class="waiting-panda">  Red pandas are fetching your images ...</p>',
			src: 'http://25.media.tumblr.com/tumblr_ly2em98lub1r3m4cbo1_400.gif'

		_.debounce renderResult( compiled ), 500
