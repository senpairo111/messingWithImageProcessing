import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

class Main{
    public static void main(String[] args) {
        try{
            DatagramSocket socket = new DatagramSocket(5162, InetAddress.getByName("0.0.0.0"));
            socket.setBroadcast(true);
            System.out.println("Listen on " + socket.getLocalAddress() + " from " + socket.getInetAddress() + " port " + socket.getBroadcast());
            byte[] buf = new byte[24];
            DatagramPacket packet = new DatagramPacket(buf, buf.length);

            while (true) {
                socket.receive(packet);
                double[] locals = new double[]{(ByteBuffer.wrap(packet.getData()).order(ByteOrder.LITTLE_ENDIAN).getDouble()),
                    (ByteBuffer.wrap(packet.getData()).order(ByteOrder.LITTLE_ENDIAN).getDouble(8)),
                    (ByteBuffer.wrap(packet.getData()).order(ByteOrder.LITTLE_ENDIAN).getDouble(16))};
                    System.out.println(String.format("x: %s, y: %s, z: %s", locals[0], locals[1], locals[2]));
            }
        }
        catch (Exception e){
            e.printStackTrace();
        }
    }
}
