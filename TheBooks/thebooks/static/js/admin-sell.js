function addOrder() {
    let sachId = document.getElementById('sachId').value;
    fetch(`/api/don_hang/${sachId}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        let bookItem = document.getElementById(`book${data.sach.id}`);
        if (bookItem != null) {
            let quantityBook = document.getElementById(`quantity-book${data.sach.id}`);
            quantityBook.value = data.sach.so_luong;
        } else {
            let item = document.getElementById('startRow');
            item.innerHTML += `<tr id="book${data.sach.id}">
                                    <th class="align-middle">${data.sach.id}</th>
                                    <th class="align-middle">${data.sach.ten}</th>
                                    <th class="align-middle">${data.sach.the_loai}</th>
                                    <th class="align-middle w-25"><input type="number" id="quantity-book${data.sach.id}" onblur="updateOrder({{ d.id }}, this)" class="form-control w-100" name="soLuong" id="soLuong" value="${data.sach.so_luong}"/></th>
                                    <th class="align-middle">${data.sach.gia.toLocaleString('en')}</th>
                                    <th>
                                        <button onclick="deleteOrder({{ d.id }}, this)" class="btn btn-danger">&times;</button>
                                    </th>
                                </tr>`;
        }

        location.reload();

        let orderCount = document.getElementById('order-count');
        let orderAmount = document.getElementById('order-amount');

        orderCount.innerText = data.thong_tin.tong_so_luong;
        orderAmount.innerText = data.thong_tin.tong_tien.toLocaleString('en');
    })
}

function updateOrder(id, obj) {
    obj.disable = true;

    fetch(`/api/don_hang/${id}`, {
        method: 'put',
        body: JSON.stringify({
            'so_luong': obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        obj.disable = false;

        let orderCount = document.getElementById('order-count');
        let orderAmount = document.getElementById('order-amount');

        orderCount.innerText = data.tong_so_luong;
        orderAmount.innerText = data.tong_tien.toLocaleString('en');
    })
}

function deleteOrder(id, obj) {
    fetch(`/api/don_hang/${id}`, {
        method: 'delete'
    }).then(res => res.json()).then(data => {
        obj.disable = true;

        let orderCount = document.getElementById('order-count');
        let orderAmount = document.getElementById('order-amount');

        orderCount.innerText = data.tong_so_luong;
        orderAmount.innerText = data.tong_tien.toLocaleString('en');

        let bookItem = document.getElementById(`book${id}`);
        bookItem.style.display = 'none';
    })
}

function findCustomer() {
    let sdt = document.getElementById('phone').value
    fetch(`/api/khach_hang/${sdt}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        let customerInfo = document.getElementById('customer-info');
        if (data.id != undefined) {
            customerInfo.innerHTML = `<h3 class="col-md-12">Thông tin khách hàng:</h3>
                                        <ul class="list-group col-md-6"> 
                                          <li class="list-group-item">Mã khách hàng: <span id="khach-hang-id">${data.id}</span></li>
                                          <li class="list-group-item">Họ tên: ${data.ten}</li>
                                          <li class="list-group-item">Số điện thoại: ${data.sdt}</li>
                                          <li class="list-group-item">Địa chỉ: ${data.dia_chi}</li>
                                        </ul>`
        } else {
            customerInfo.innerHTML += `<div class='alert alert-danger col-md-12 mx-3 mt-3'>Không tìm thấy khách hàng</div>`
        }
    })
}

function pay() {
    let item = document.getElementById('khach-hang-id').innerText
    khachHangId = parseInt(item)
    fetch('/api/don_hang/dat_hang', {
        method: 'post',
        body: JSON.stringify({
            'khach_hang_id': khachHangId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        if (data.status === 200) {
            alert('Đặt hàng thành công');
            location.reload();
        }
        else
            alert(data.error_message);
    })
}