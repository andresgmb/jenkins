package cl.destacame.addresses;

import org.rosuda.REngine.REXP;
import org.rosuda.REngine.REXPMismatchException;
import org.rosuda.REngine.Rserve.RConnection;
import org.rosuda.REngine.Rserve.RserveException;

/*
 * Clase creada para conectarse con un servidor de Rserve, en que se puedan
 * ejecutar funciones en el lenguaje R. Permite la conexión con instancias
 * abiertas y con instancias que requieran autenticación mediante usuario
 * y contraseña.
 *
 * @author  Gabriel Ruiz
 * @version 1.0
 * @since   2017-05-29
 */
public class RServerConnector {
	private String username;
	private String password;

	/*
     * Constructor de la clase, sin datos de autenticación en Rserve.
     */
	public RServerConnector(){}

	/*
     * Constructor de la clase, con los datos de autenticación como parámetros.
     *
     * @param username	Nombre de usuario para conectarse al servidor de Rserve.
     * @param password	Contraseña para conectarse al servidor de Rserve.
     */
	public RServerConnector(String username, String password) {
		this.setUsername(username);
		this.password = password;
	}

	/*
     * Función que evalúa una expresión enviada por parámetro en el ambiente de R.
     * Si el servidor requiere autenticación, utiliza las credenciales que la clase
     * tiene como atributo.
     *
     * @param 	expression	Expresión a ser evaluada. Debe ser una expresion válida,
     *						o el servidor arrojará un error.
     * @return				Resultado de la ejecución en el servidor de R, siempre
     *						como string.
     */
	public String evaluate(String expression) {
		RConnection conn = null;
		String result = null;
		try {
			conn = new RConnection(
				System.getenv("R_HOST"),
				Integer.parseInt(System.getenv("R_PORT"))
			);
			if(conn.needLogin())
				conn.login(this.username, this.password);
			REXP rexp = conn.eval(expression);
			result = rexp.asString();
		} catch (RserveException e) {
			e.printStackTrace();
		} catch (REXPMismatchException e) {
			e.printStackTrace();
		} finally {
			if (conn != null && conn.isConnected())
				conn.close();
		}
		return result;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}


}
