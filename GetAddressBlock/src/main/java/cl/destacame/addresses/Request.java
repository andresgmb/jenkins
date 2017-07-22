package cl.destacame.addresses;

/*
 * Clase que se asigna los datos recibidos como parámetros en una llamada
 * a la función 'GetAddressBlock' en AWS Lambda. Dado que las funciones
 * en Java para AWS Lambda no permiten enviar más de tres parámetros, se
 * se debe usar el patrón Request/Response objects.
 *
 * @see     http://docs.aws.amazon.com/lambda/latest/dg/java-handler-using-predefined-interfaces.html
 * @author  Gabriel Ruiz
 * @version 1.0
 * @since   2017-05-29
 */
public class Request {
    private String target;
    private float longitude;
    private float latitude;
    private int address;
    private String reg;
    private String cut;
    private boolean debug = false;
    private String location_type;

    public void setTarget(String target){
        this.target = target;
    };

    public void setLongitude(float longitude){
        this.longitude = longitude;
    };

    public void setLatitude(float latitude){
        this.latitude = latitude;
    };

    public void setAddress(int address){
        this.address = address;
    };

    public void setReg(String reg){
        this.reg = reg;
    };

    public void setCut(String cut){
        this.cut = cut;
    };

    public void setDebug(boolean debug){
        this.debug = debug;
    };

    public void setLocation_type(String location_type){
        this.location_type = location_type;
    };

    public String getTarget(){
        return this.target;
    };

    public float getLongitude(){
        return this.longitude;
    };

    public float getLatitude(){
        return this.latitude;
    };

    public int getAddress(){
        return this.address;
    };

    public String getReg(){
        return this.reg;
    };

    public String getCut(){
        return this.cut;
    };

    public boolean isDebug(){
        return this.debug;
    };

    public String getLocation_type(){
        return this.location_type;
    };

    /*
     * Constructor de la clase, con todos los datos posibles a recibir.
     *
     * @param target        Sistema al que se deben ir a guardar los datos, como
     *                      Pandora, Ares, Production, etc.
     * @param longitude     Longitud de la coordenada entregada por la API de Google
     *                      Maps para esta dirección.
     * @param latitude      Latitud de la coordenada entregada por la API de Google
     *                      Maps para esta dirección.
     * @param address       ID del registro de dirección en base de datos del target.
     * @param reg           El nombre de la región donde se realiza la búsqueda, en
     *                      formato RegXX (Ej: Reg01, Reg13.)
     * @param cut           El Código único territorial de la comuna donde se realizará
     *                      la búsqueda. Si las coordenadas no están no esta comuna,
     *                      la llamada a Rserve arrojará un resultado 'Error'.
     * @param debug         Si se deben mostrar los logs de Debug o no. Por defecto,
     *                      es 'true'
     * @param location_type Tipo de ubicación que entrega la API de Google
     *                      Maps para una dirección.
     */
    public Request(
            String target,
            float longitude,
            float latitude,
            int address,
            String reg,
            String cut,
            boolean debug,
            String location_type) {
        this.target = target;
        this.longitude = longitude;
        this.latitude = latitude;
        this.address = address;
        this.reg = reg;
        this.cut = cut;
        this.debug = debug;
        this.location_type = location_type;
    }

    /*
     * Constructor de la clase, con todos los datos posibles a recibir.
     *
     * @param target        Sistema al que se deben ir a guardar los datos, como
     *                      Pandora, Ares, Production, etc.
     * @param longitude     Longitud de la coordenada entregada por la API de Google
     *                      Maps para esta dirección.
     * @param latitude      Latitud de la coordenada entregada por la API de Google
     *                      Maps para esta dirección.
     * @param address       ID del registro de dirección en base de datos del target.
     * @param reg           El nombre de la región donde se realiza la búsqueda, en
     *                      formato RegXX (Ej: Reg01, Reg13.)
     * @param cut           El Código único territorial de la comuna donde se realizará
     *                      la búsqueda. Si las coordenadas no están no esta comuna,
     *                      la llamada a Rserve arrojará un resultado 'Error'.
     * @param location_type Tipo de ubicación que entrega la API de Google
     *                      Maps para una dirección.
     */
    public Request(
            String target,
            float longitude,
            float latitude,
            int address,
            String reg,
            String cut,
            String location_type) {
        this.target = target;
        this.longitude = longitude;
        this.latitude = latitude;
        this.address = address;
        this.reg = reg;
        this.cut = cut;
        this.debug = false;
        this.location_type = location_type;
    }

    public Request() {}
}
