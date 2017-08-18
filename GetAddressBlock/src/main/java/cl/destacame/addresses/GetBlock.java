package cl.destacame.addresses;

import java.io.IOException;
import java.util.Locale;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;

/*
 * Clase que implementa el handler de la función de AWS Lambda.
 * Su función principal consiste en buscar la cuadra a la que
 * pertenece un set de coordenadas...
 * @author  Gabriel Ruiz
 * @version 1.0
 * @since   2017-05-29
 */
public class GetBlock implements RequestHandler<Request, Response> {

    /*
     * Función que recibe los parámetros enviados a la función de AWS Lambda,
     * previamente parseados a un objeto Request, y ejecuta la búsqueda
     * de la cuadra.
     *
     * @param   request Objeto con los parámetros enviados a la función.
     * @param   context Contexto de AWS Lambda.
     * @return          Objeto Response, con un solo valor, la respuesta de
     *                  Rserve a la ejecución de un comando.
     */
	public Response handleRequest(Request request, Context context) {
		String token;
		String host;
		String result;
        if (request.isDebug())
            this.printArgs(request);
		DepotConnector depotConnector;
		LambdaLogger logger = context.getLogger();
		logger.log("Starting evaluation for address " + request.getAddress());
		RServerConnector conn = new RServerConnector(
			System.getenv("R_USERNAME"),
			System.getenv("R_PASSWORD")
		);
		String exp = "GEO_MZ(%f, %f, %d, \"%s\", \"%s\", \"0\")";
		exp = String.format(
			Locale.getDefault(),
			exp,
			request.getLongitude(),
			request.getLatitude(),
			request.getAddress(),
			request.getReg(),
			request.getCut()
		);
		result = conn.evaluate(exp);
        if (result == null || result.equals("Error")) {
            logger.log("Sin respuesta de Rserve");
            return new Response("");
        }
		host = System.getenv(String.format("HOST_%s",
			request.getTarget().toUpperCase()));
    	token = System.getenv(String.format("TOKEN_%s",
    		request.getTarget().toUpperCase()));
		if(host == null || token == null) {
			logger.log(String.format("Target \"%s\" not allowed",
				request.getTarget()));
			return new Response(result);
    	}
    	depotConnector = new DepotConnector(host, token);
    	try {
    		int statusCode = depotConnector.patch(request, result);
    		if(statusCode == 200) {
    			logger.log(String.format("Address %d successfully updated.", request.getAddress()));
    		} else {
    			logger.log(String.format(
    				"API %s throws status code %d at update for address %d.",
    				request.getTarget(),
    				statusCode,
    				request.getAddress()));
    		}
    	} catch(IOException e){
    		logger.log(e.getMessage());
    	}
		logger.log("Finished evaluation for address " + request.getAddress());
		return new Response(result);
	}

    private void printArgs(Request request) {
        System.out.println(request.getLongitude());
        System.out.println(request.getLatitude());
        System.out.println(request.getAddress());
        System.out.println(request.getReg());
        System.out.println(request.getCut());
        System.out.println(request.getLocation_type());
    }
}
