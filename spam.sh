#!/bin/bash

detect_distro() {
    if [[ "$OSTYPE" == linux-android* ]]; then
            distro="termux"
    fi

    if [ -z "$distro" ]; then
        distro=$(ls /etc | awk 'match($0, "(.+?)[-_](?:release|version)", groups) {if(groups[1] != "os") {print groups[1]}}')
    fi

    if [ -z "$distro" ]; then
        if [ -f "/etc/os-release" ]; then
            distro="$(source /etc/os-release && echo $ID)"
        elif [ "$OSTYPE" == "darwin" ]; then
            distro="darwin"
        else 
            distro="invalid"
        fi
    fi
}

pause() {
    read -n1 -r -p "digite pato e da enter para continuar..." key
}
banner() {
    clear
    echo -e "\e[1;31m"
    if ! [ -x "$(command -v figlet)" ]; then
        echo 'Introducing TBomb'
    else
        figlet TBomb
    fi
    if ! [ -x "$(command -v toilet)" ]; then
        echo -e "Criado Por pato "
    else
        echo -e "Kiba na vagabuda"
        toilet -f mono12 -F border SpeedX
    fi
    echo -e "\e[1;34m For Any Queries Join Me!!!\e[0m"
    echo -e "\e[1;32m           Telegram: https://t.me/TBombChat \e[0m"
    echo -e "\e[4;32m   YouTube: https://www.youtube.com/c/SpeedXTech \e[0m"
    echo " "

}

init_environ(){
    declare -A backends; backends=(
        ["arch"]="pacman -S --noconfirm"
        ["debian"]="apt-get -y install"
        ["ubuntu"]="apt -y install"
        ["termux"]="apt -y install"
        ["fedora"]="yum -y install"
        ["redhat"]="yum -y install"
        ["SuSE"]="zypper -n install"
        ["sles"]="zypper -n install"
        ["darwin"]="brew install"
        ["alpine"]="apk add"
    )

    INSTALL="${backends[$distro]}"

    if [ "$distro" == "termux" ]; then
        PYTHON="python"
        SUDO=""
    else
        PYTHON="python3"
        SUDO="sudo"
    fi
    PIP="$PYTHON -m pip"
}

install_deps(){
    
    packages=(openssl git $PYTHON $PYTHON-pip figlet toilet)
    if [ -n "$INSTALL" ];then
        for package in ${packages[@]}; do
            $SUDO $INSTALL $package
        done
        $PIP install -r requirements.txt
    else
        echo "Não foi possível instalar dependências."
        echo "Certifique-se de ter git, python3, pip3 e requisitos instalados."
        echo "Então você pode executar bomber.py ."
        exit
    fi
}

banner
pause
detect_distro
init_environ
if [ -f .update ];then
    echo "Todos os requisitos encontrados...."
else
    echo 'instalaando requisitos....'
    echo .
    echo .
    install_deps
    echo Feito Por Pato > .update
    echo 'instalado....'
    pause
fi
while :
do
    banner
    echo -e "By Pato"
    echo -e "Sem Kibe em filadaputa"
    echo -e "\e[4;31m Leia a porra das isntruçoes !!! \e[0m"
    echo " "
    echo "digite 1 para ir para a tela de spam de sms "
    echo "digite 2 para sair "
    read ch
    clear
    if [ $ch -eq 1 ];then
        $PYTHON bomber.py --sms
        exit
    elif [ $ch -eq 2 ];then
        $PYTHON bomber.py --call
        exit
    elif [ $ch -eq 3 ];then
        $PYTHON bomber.py --mail
        exit
    elif [ $ch -eq 4 ];then
        echo -e "\e[1;34m Baixando os arquivos mais recentes..."
        rm -f .update
        $PYTHON bomber.py --update
        echo -e "\e[1;34m Iniciando dnv..."
        pause
        exit
    elif [ $ch -eq 5 ];then
        banner
        exit
    else
        echo -e "\e[4;32m entrada inválida !!! \e[0m"
        pause
    fi
done
