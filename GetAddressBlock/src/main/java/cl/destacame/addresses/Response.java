package cl.destacame.addresses;

/*
 * Clase que se asigna los datos que la función 'GetAddressBlock' de AWS
 * Lambda enviará como respuesta, en caso de ser llamada de forma síncrona.
 *
 * @see     http://docs.aws.amazon.com/lambda/latest/dg/java-handler-using-predefined-interfaces.html
 * @author  Gabriel Ruiz
 * @version 1.0
 * @since   2017-05-29
 */
public class Response {
    private String block;

    public void setBlock(String block){
        this.block = block;
    };

    public String getBlock(){
        return this.block;
    };

    /*
     * Constructor de la clase, con todos los datos posibles a recibir.
     *
     * @param block Identificador de la cuadra que R arrojó como respuesta.
     */
    public Response(String block) {
        this.block = block;
    }

    public Response() {}
}
