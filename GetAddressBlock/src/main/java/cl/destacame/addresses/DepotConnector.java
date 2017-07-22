package cl.destacame.addresses;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.commons.httpclient.methods.StringRequestEntity;
import org.codehaus.jackson.map.ObjectMapper;

/*
 * Clase creada especialmente para enviar los datos de la cuadra, coordenadas,
 * etc., al servidor que los almacena en la base de datos. En el caso de Pandora
 * y Ares es el mismo servidor de aplicación. En el caso de Producción, se usa
 * el servidor Hermes.
 *
 * @author  Gabriel Ruiz
 * @version 1.0
 * @since   2017-05-26
 */
public class DepotConnector {
    private String authToken;
    private String url;
    private String host;

    public DepotConnector(){}

    /*
     * Constructor de la clase, con los datos de conexión como parámetros.
     *
     * @param host      La URL del servicio donde se enviarán los datos
     *                  resultantes.
     * @param authToken El token de autenticación para conectarse al servicio
     *                  de almacenamiento de datos de Destácame.
     */
    public DepotConnector(String host, String authToken) {
        this.authToken = authToken;
        this.setHost(host);
    }

    /*
     * Función que permite enviar una consulta HTTP PATCH (no UPDATE),
     * para hacer una actualización parcial de los datos de una dirección
     * en la REST API de Destácame.
     *
     * @param   request     Objeto representando a la consulta recibida por
     *                      la función de AWS Lambda, con todos sus parámetros.
     * @param   blockNumber Identificador de la cuadra a la que pertenece
     *                      el set de coordenadas enviado.
     * @return              El código HTTP resultante de la consulta al servidor,
     *                      o cero, si no se pudo llevar a cabo.
     */
    public int patch(Request request, String blockNumber) throws IOException {
    	int statusCode = 0;
    	String url = String.format(this.url, request.getAddress());
    	HttpClient client = new HttpClient();
    	PostMethod httpPatch = createPost(url + "?_HttpMethod=PATCH");
    	Map<String, Object> innerMap = new HashMap<String, Object>();
    	innerMap.put("number", blockNumber);

    	Map<String, Object> accUpdate = new HashMap<String, Object>();
		accUpdate.put("latitude", request.getLatitude());
		accUpdate.put("longitude", request.getLongitude());
		accUpdate.put("location_type", request.getLocation_type());
        accUpdate.put("block", blockNumber);
		accUpdate.put("block_data", innerMap);
		ObjectMapper mapper = new ObjectMapper();

    	httpPatch.setRequestEntity(
    		new StringRequestEntity(
	    		mapper.writeValueAsString(accUpdate),
	    		"application/json",
	    		"UTF-8"
    		)
		);
		try {
	      	statusCode = client.executeMethod(httpPatch);

	      	if (statusCode != 200) {
	      		  System.err.println("Method failed: " + httpPatch.getStatusLine());
	      	}
	      	if (request.isDebug()) {
	      		byte[] responseBody = httpPatch.getResponseBody();
	      		System.out.println(new String(responseBody));
	      	}

    	} catch (HttpException e) {
    	  	System.err.println("Fatal protocol violation: " + e.getMessage());
    	  	if (request.isDebug())
    	  		e.printStackTrace();
    	} catch (IOException e) {
    	  	System.err.println("Fatal transport error: " + e.getMessage());
    	  	if (request.isDebug())
    	  		e.printStackTrace();
    	} finally {
      		httpPatch.releaseConnection();
    	}
		return statusCode;
	}

    /*
     * Función que crea un objeto PostMethod de la librería Apache HTTP
     * para ser usado como PATCH, con headers de autenticación, y para
     * declarar su contenido como JSON.
     *
     * @param   url URL de la REST API para enviar los datos.
     * @return      PostMethod alterado.
     */
	private PostMethod createPost(String url) {
	    PostMethod post = new PostMethod(url){
			@Override public String getName() { return "PATCH"; }
		};
	    post.setRequestHeader("Authorization", "Token " + this.authToken);
	    post.setRequestHeader("Content-Type", "application/json");
	    return post;
	}

	public void setHost(String host){
        this.host = host;
        this.url = host + "/api/addresses/%d/";
    };

    public String getHost(){
        return this.host;
    };

}
